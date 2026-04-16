"""
API Cost Estimation Service

Estimates API costs based on current provider pricing and usage patterns.
Maintains up-to-date pricing information and provides accurate cost calculations.

Issue #253 CORE-KEYS-COST-ANALYTICS
"""

import logging
from datetime import datetime
from decimal import Decimal
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CostEstimator:
    """Estimates API costs based on usage and current pricing"""

    def __init__(self):
        """Initialize cost estimator with current pricing data"""
        # Pricing as of October 2025 (update regularly!)
        self.pricing = {
            "openai": {
                "gpt-4": {
                    "prompt": Decimal("0.03"),  # per 1K tokens
                    "completion": Decimal("0.06"),  # per 1K tokens
                },
                "gpt-4-turbo": {"prompt": Decimal("0.01"), "completion": Decimal("0.03")},
                "gpt-4o": {"prompt": Decimal("0.005"), "completion": Decimal("0.015")},
                "gpt-3.5-turbo": {"prompt": Decimal("0.0015"), "completion": Decimal("0.002")},
                "gpt-3.5-turbo-instruct": {
                    "prompt": Decimal("0.0015"),
                    "completion": Decimal("0.002"),
                },
            },
            "anthropic": {
                "claude-3-opus": {"prompt": Decimal("0.015"), "completion": Decimal("0.075")},
                "claude-3-sonnet": {"prompt": Decimal("0.003"), "completion": Decimal("0.015")},
                "claude-haiku-4-5": {"prompt": Decimal("0.001"), "completion": Decimal("0.005")},
                "claude-3.5-sonnet": {"prompt": Decimal("0.003"), "completion": Decimal("0.015")},
            },
            "perplexity": {
                "llama-3.1-sonar-small": {
                    "prompt": Decimal("0.0002"),
                    "completion": Decimal("0.0002"),
                },
                "llama-3.1-sonar-large": {
                    "prompt": Decimal("0.001"),
                    "completion": Decimal("0.001"),
                },
                "llama-3.1-sonar-huge": {
                    "prompt": Decimal("0.005"),
                    "completion": Decimal("0.005"),
                },
            },
            "gemini": {
                "gemini-pro": {"prompt": Decimal("0.0005"), "completion": Decimal("0.0015")},
                "gemini-pro-vision": {"prompt": Decimal("0.0025"), "completion": Decimal("0.01")},
            },
        }

        # Default pricing for unknown models
        self.default_pricing = {"prompt": Decimal("0.002"), "completion": Decimal("0.004")}

        # Pricing last updated
        self.pricing_updated = datetime(2026, 4, 15)

    def estimate_cost(
        self, provider: str, model: str, prompt_tokens: int, completion_tokens: int
    ) -> Decimal:
        """
        Estimate cost for API call

        Args:
            provider: Provider name (openai, anthropic, etc.)
            model: Model name (gpt-4, claude-3-opus, etc.)
            prompt_tokens: Number of input tokens
            completion_tokens: Number of output tokens

        Returns:
            Estimated cost in USD
        """
        try:
            # Normalize provider and model names
            provider = provider.lower().strip()
            model = model.lower().strip()

            # Get pricing for provider/model
            pricing = self._get_model_pricing(provider, model)

            # Calculate costs
            prompt_cost = (Decimal(prompt_tokens) / 1000) * pricing["prompt"]
            completion_cost = (Decimal(completion_tokens) / 1000) * pricing["completion"]

            total_cost = prompt_cost + completion_cost

            # Round to 4 decimal places
            return total_cost.quantize(Decimal("0.0001"))

        except Exception as e:
            logger.error(f"Failed to estimate cost for {provider}/{model}: {e}")
            # Return conservative estimate
            return Decimal("0.01")

    def _get_model_pricing(self, provider: str, model: str) -> Dict[str, Decimal]:
        """Get pricing for specific provider/model combination"""

        # Check if provider exists
        if provider not in self.pricing:
            logger.warning(f"Unknown provider '{provider}', using default pricing")
            return self.default_pricing

        provider_pricing = self.pricing[provider]

        # Check if model exists
        if model not in provider_pricing:
            # Try to find similar model
            similar_model = self._find_similar_model(provider, model)
            if similar_model:
                logger.info(f"Using pricing for similar model '{similar_model}' for '{model}'")
                return provider_pricing[similar_model]

            logger.warning(
                f"Unknown model '{model}' for provider '{provider}', using default pricing"
            )
            return self.default_pricing

        return provider_pricing[model]

    def _find_similar_model(self, provider: str, model: str) -> Optional[str]:
        """Try to find similar model for pricing"""
        provider_models = self.pricing.get(provider, {})

        # Common model name variations
        model_mappings = {
            "gpt-4-0125-preview": "gpt-4-turbo",
            "gpt-4-1106-preview": "gpt-4-turbo",
            "gpt-4-turbo-preview": "gpt-4-turbo",
            "claude-3-opus-20240229": "claude-3-opus",
            "claude-3-sonnet-20240229": "claude-3-sonnet",
            "claude-haiku-4-5-20251001": "claude-haiku-4-5",
        }

        # Check direct mapping
        if model in model_mappings and model_mappings[model] in provider_models:
            return model_mappings[model]

        # Check for partial matches
        for known_model in provider_models:
            if known_model in model or model in known_model:
                return known_model

        return None

    def get_model_pricing_info(self, provider: str, model: str) -> Dict:
        """Get detailed pricing information for a model"""
        try:
            provider = provider.lower().strip()
            model = model.lower().strip()

            pricing = self._get_model_pricing(provider, model)

            return {
                "provider": provider,
                "model": model,
                "prompt_price_per_1k": float(pricing["prompt"]),
                "completion_price_per_1k": float(pricing["completion"]),
                "currency": "USD",
                "last_updated": self.pricing_updated.isoformat(),
            }

        except Exception as e:
            logger.error(f"Failed to get pricing info: {e}")
            return {"error": str(e)}

    def compare_model_costs(
        self,
        models: list[tuple[str, str]],  # [(provider, model), ...]
        prompt_tokens: int = 1000,
        completion_tokens: int = 1000,
    ) -> list[Dict]:
        """Compare costs across different models for given token usage"""

        comparisons = []

        for provider, model in models:
            cost = self.estimate_cost(provider, model, prompt_tokens, completion_tokens)
            pricing_info = self.get_model_pricing_info(provider, model)

            comparisons.append(
                {
                    "provider": provider,
                    "model": model,
                    "estimated_cost": float(cost),
                    "prompt_price_per_1k": pricing_info.get("prompt_price_per_1k", 0),
                    "completion_price_per_1k": pricing_info.get("completion_price_per_1k", 0),
                    "cost_per_1k_tokens": float(cost * 1000 / (prompt_tokens + completion_tokens)),
                }
            )

        # Sort by cost (lowest first)
        comparisons.sort(key=lambda x: x["estimated_cost"])

        return comparisons

    def get_cost_savings_recommendations(
        self, current_provider: str, current_model: str, monthly_tokens: int
    ) -> list[str]:
        """Generate cost savings recommendations"""

        recommendations = []
        current_cost = self.estimate_cost(
            current_provider, current_model, monthly_tokens // 2, monthly_tokens // 2
        )

        # Compare with cheaper alternatives
        alternatives = [
            ("openai", "gpt-3.5-turbo"),
            ("anthropic", "claude-haiku-4-5"),
            ("perplexity", "llama-3.1-sonar-small"),
        ]

        for provider, model in alternatives:
            if provider == current_provider and model == current_model:
                continue

            alt_cost = self.estimate_cost(provider, model, monthly_tokens // 2, monthly_tokens // 2)

            if alt_cost < current_cost:
                savings = current_cost - alt_cost
                savings_percent = (savings / current_cost) * 100

                recommendations.append(
                    f"💰 Switch to {provider}/{model} for ${savings:.2f}/month savings ({savings_percent:.0f}%)"
                )

        # General recommendations
        if current_cost > Decimal("10.00"):
            recommendations.extend(
                [
                    "💡 Use cheaper models for simple tasks (classification, summarization)",
                    "💡 Implement response caching to reduce duplicate requests",
                    "💡 Optimize prompts to reduce token usage",
                ]
            )

        return recommendations

    def estimate_monthly_cost(
        self,
        provider: str,
        model: str,
        daily_requests: int,
        avg_prompt_tokens: int,
        avg_completion_tokens: int,
    ) -> Dict:
        """Estimate monthly costs based on usage patterns"""

        daily_cost = self.estimate_cost(
            provider,
            model,
            avg_prompt_tokens * daily_requests,
            avg_completion_tokens * daily_requests,
        )

        monthly_cost = daily_cost * 30
        yearly_cost = daily_cost * 365

        return {
            "daily_cost": float(daily_cost),
            "monthly_cost": float(monthly_cost),
            "yearly_cost": float(yearly_cost),
            "cost_per_request": float(daily_cost / daily_requests) if daily_requests > 0 else 0,
            "provider": provider,
            "model": model,
        }

    def get_all_pricing(self) -> Dict:
        """Get all current pricing information"""
        # Convert Decimal to float for JSON serialization
        pricing_json = {}

        for provider, models in self.pricing.items():
            pricing_json[provider] = {}
            for model, prices in models.items():
                pricing_json[provider][model] = {
                    "prompt": float(prices["prompt"]),
                    "completion": float(prices["completion"]),
                }

        return {
            "pricing": pricing_json,
            "last_updated": self.pricing_updated.isoformat(),
            "currency": "USD",
            "unit": "per 1K tokens",
        }
