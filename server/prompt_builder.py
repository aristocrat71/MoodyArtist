def build_creative_prompt(experience: str, artform: str, moods: list) -> str:
    # Experience level descriptions
    experience_descriptions = {
        "Beginner": "suitable for beginners with simple techniques and easy-to-follow steps",
        "Somewhat good?": "for artists with some experience, using intermediate techniques",
        "Experttt": "for experienced artists who can handle complex techniques and detailed work"
    }
    
    experience_desc = experience_descriptions.get(experience, "suitable for all levels")
    
    # Build the comprehensive prompt
    prompt = f"""<s>[INST] You are a creative art instructor and idea generator.

        Create a unique, accessible art project idea with these specifications:

        Experience Level: {experience}
        Art Form: {artform}
        Mood/Theme: {', '.join(moods)}

        Please provide:
        1. A project title
        2. A brief description (2–3 sentences)
        3. Key materials needed (3–5 items)
        4. Simple steps to create it (3–4 steps)

        Make it inspiring, fun, and suited to the specified experience level and mood/theme.
        Format your response clearly to engage any artist. [/INST]"""

    
    return prompt 