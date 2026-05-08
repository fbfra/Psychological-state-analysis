def reserve_context(total_window:int, prompt_tokens:int, output_tokens:int)->int:
    """
    Return how many tokens remain for retrieval and tool context.
    """
    remaining = total_window - prompt_tokens - output_tokens
    return max(0, remaining)

window=128000
prompt=1800
completion_budget=1200
retrieval_budget = reserve_context(window, prompt, completion_budget)
print({"retrieval budget": retrieval_budget})