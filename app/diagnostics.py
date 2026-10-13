def diagnose(read_score, listen_score):
    read_score = float(read_score)
    listen_score = float(listen_score)
    
    if listen_score >= 0.7 and read_score < 0.7:
        return "🔤 Decoding Gap: You understand the story when you hear it, but struggle to read the words."
    elif listen_score < 0.7 and read_score < 0.7:
        return "🧠 Comprehension Gap: The story is hard to understand in both modes."
    else:
        return "✅ On Track: Great job! You are comprehending the text well."