# LLM-based input → traits extraction
from .llm_client import GeminiClient
from .model import SoulProfile
from pydantic import ValidationError
import os
from datetime import datetime

def validate_and_repair_profile(data: dict) -> SoulProfile:
    try:
        return SoulProfile(**data)
    except ValidationError:
        # Repair missing fields
        repaired_data = {field: data.get(field, None) for field in SoulProfile.model_fields.keys()}

        for field, field_info in SoulProfile.model_fields.items():
            expected_type = field_info.annotation
            if repaired_data[field] is None and expected_type == list:
                repaired_data[field] = []

        return SoulProfile(**repaired_data)

def extract_profile_from_input(user_input: str) -> SoulProfile:
    client = GeminiClient()

    try:
        extracted_data = client.extract_identity_traits(user_input)

        if not isinstance(extracted_data, dict):
            raise TypeError(f"Expected a dictionary from LLM, but got {type(extracted_data)}")

        # Use validation and repair here
        return validate_and_repair_profile(extracted_data)

    except (ValueError, TypeError) as e:
        print(f"Error extracting profile: {e}")
        raise  # You can choose to handle differently if you prefer

def save_profile_to_json(profile: SoulProfile, base_dir: str = "data"):
    try:
        profile_dir = os.path.join(base_dir, "soul_profiles")
        os.makedirs(profile_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(profile_dir, f"soul_profile_{timestamp}.json")
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(profile.model_dump_json(indent=2))
        return filename
    except OSError as e:
        raise RuntimeError(f"Failed to save profile: {e}")