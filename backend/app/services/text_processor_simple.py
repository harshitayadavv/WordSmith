import time
import logging
from typing import Optional, Dict, Any
import asyncio
import httpx
from app.core.config import settings
from app.models.schemas import TransformationType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleTextProcessor:
    """Simple text processor using direct Groq API calls without LangChain."""
    
    def __init__(self):
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {settings.groq_api_key}",
            "Content-Type": "application/json"
        }
        
        # Define transformation prompts
        self.transformation_prompts = {
            TransformationType.GRAMMAR_FIX: """
            Fix the grammar, spelling, and punctuation errors in the following text while preserving its original meaning and tone:

            Text: {text}
            
            Additional instructions: {additional_instructions}
            
            Return only the corrected text without any explanations or quotes.
            """,
            
            TransformationType.FORMAL: """
            Rewrite the following text in a formal, professional tone suitable for business communication:

            Text: {text}
            
            Additional instructions: {additional_instructions}
            
            Return only the formalized text without any explanations or quotes.
            """,
            
            TransformationType.FRIENDLY: """
            Rewrite the following text in a warm, friendly, and conversational tone:

            Text: {text}
            
            Additional instructions: {additional_instructions}
            
            Return only the friendly version without any explanations or quotes.
            """,
            
            TransformationType.SHORTEN: """
            Make the following text more concise while preserving all key information and meaning:

            Text: {text}
            
            Additional instructions: {additional_instructions}
            
            Return only the shortened text without any explanations or quotes.
            """,
            
            TransformationType.EXPAND: """
            Expand and elaborate on the following text, adding relevant details and explanations while maintaining the core message:

            Text: {text}
            
            Additional instructions: {additional_instructions}
            
            Return only the expanded text without any explanations or quotes.
            """,
            
            TransformationType.BULLET: """
            Convert the following text into a clear, well-organized bullet point format:

            Text: {text}
            
            Additional instructions: {additional_instructions}
            
            Return only the bullet points without any explanations or quotes. Use • for bullet points.
            """,
            
            TransformationType.EMOJI: """
            Enhance the following text by adding appropriate emojis to make it more engaging and expressive:

            Text: {text}
            
            Additional instructions: {additional_instructions}
            
            Return only the text with emojis without any explanations or quotes.
            """,
            
            TransformationType.TWEETIFY: """
            Transform the following text into an engaging tweet (under 280 characters) with appropriate hashtags and emojis:

            Text: {text}
            
            Additional instructions: {additional_instructions}
            
            Return only the tweet without any explanations or quotes.
            """
        }
    
    async def _call_groq_api(self, prompt: str) -> str:
        """Make a direct API call to Groq."""
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "model": settings.default_model,
            "temperature": settings.temperature,
            "max_tokens": settings.max_tokens,
            "stream": False
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                json=payload,
                headers=self.headers,
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise Exception(f"Groq API error: {response.status_code} - {response.text}")
            
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
    
    async def transform_text(
        self,
        text: str,
        transformation_type: TransformationType,
        additional_instructions: Optional[str] = None
    ) -> Dict[str, Any]:
        """Transform text using the specified transformation type."""
        start_time = time.time()
        
        try:
            # Get the prompt template
            prompt_template = self.transformation_prompts.get(transformation_type)
            if not prompt_template:
                raise ValueError(f"Unsupported transformation type: {transformation_type}")
            
            # Format the prompt
            prompt = prompt_template.format(
                text=text,
                additional_instructions=additional_instructions or "None"
            )
            
            # Call Groq API
            logger.info(f"Transforming text with type: {transformation_type}")
            transformed_text = await self._call_groq_api(prompt)
            
            # Clean up the response
            transformed_text = transformed_text.strip()
            if transformed_text.startswith('"') and transformed_text.endswith('"'):
                transformed_text = transformed_text[1:-1]
            
            processing_time = time.time() - start_time
            
            result = {
                "original_text": text,
                "transformed_text": transformed_text,
                "transformation_type": transformation_type,
                "processing_time": round(processing_time, 2),
                "word_count_original": len(text.split()),
                "word_count_transformed": len(transformed_text.split())
            }
            
            logger.info(f"Transformation completed in {processing_time:.2f} seconds")
            return result
            
        except Exception as e:
            logger.error(f"Error during text transformation: {str(e)}")
            raise Exception(f"Text transformation failed: {str(e)}")
    
    async def batch_transform(
        self,
        texts: list,
        transformation_type: TransformationType,
        additional_instructions: Optional[str] = None
    ) -> Dict[str, Any]:
        """Transform multiple texts at once."""
        start_time = time.time()
        results = []
        successful = 0
        failed = 0
        
        # Process texts concurrently
        tasks = []
        for text in texts:
            task = self.transform_text(text, transformation_type, additional_instructions)
            tasks.append(task)
        
        # Wait for all tasks to complete
        task_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, result in enumerate(task_results):
            if isinstance(result, Exception):
                logger.error(f"Failed to transform text: {texts[i][:50]}... Error: {str(result)}")
                failed += 1
                results.append({
                    "original_text": texts[i],
                    "transformed_text": f"Error: {str(result)}",
                    "transformation_type": transformation_type,
                    "processing_time": 0,
                    "word_count_original": len(texts[i].split()),
                    "word_count_transformed": 0
                })
            else:
                successful += 1
                results.append(result)
        
        total_processing_time = time.time() - start_time
        
        return {
            "results": results,
            "total_processing_time": round(total_processing_time, 2),
            "successful_transformations": successful,
            "failed_transformations": failed
        }
    
    async def health_check(self) -> Dict[str, str]:
        """Check if the Groq API is accessible."""
        try:
            test_prompt = "Say 'Hello' if you can hear me."
            result = await self._call_groq_api(test_prompt)
            if result:
                return {"status": "healthy", "message": "Groq API is accessible"}
            else:
                return {"status": "unhealthy", "message": "Groq API returned empty response"}
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {"status": "unhealthy", "message": f"Groq API error: {str(e)}"}

# Global text processor instance
text_processor = SimpleTextProcessor()