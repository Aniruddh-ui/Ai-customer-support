from jiwer import wer, cer

# Reference: what a human would say
reference_text = "I need to cancel my order"
# Hypothesis: what your STT (Speech to Text) system transcribed
stt_output = "I need cancel my order"

# Calculate Word Error Rate (WER)
wer_score = wer(reference_text, stt_output)

print(f"Reference (Human): {reference_text}")
print(f"Hypothesis (STT Output): {stt_output}")
print(f"Word Error Rate (WER): {wer_score:.2f}")

