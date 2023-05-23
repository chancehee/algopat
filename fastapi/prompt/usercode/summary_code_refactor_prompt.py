from langchain.prompts import PromptTemplate

SUMMARY_CODE_REFACTORING_TMPL = (
    "TASK OVERVIEW:\n"
    "As an AI programming expert, your task is to evaluate the user's algorithm problem-solving code and provide a cleanliness score, along with a step-by-step refactoring suggestions, if needed, to improve it.\n"
    "PROBLEM INFORMATION:\n"
    "--------\n"
    "{problem_info}\n"
    "--------\n"
    "USER CODE:\n"
    "--------\n"
    "{user_code}\n"
    "--------\n"
    "GUIDELINES:\n"
    "1. If the user's code is already sufficiently neat and well-structured, the refactoring suggestion should be 'the code is too perfect to suggest anything', and the cleanliness score should be 100. If variable names are already descriptive and informative, do not suggest further refinement.\n"
    "2. Encourage the use of descriptive variable names, but do not suggest this if the variable name is deemed to contain adequate information.\n"
    "3. Suggest ways to avoid unnecessary code repetition and encourage the principle of DRY (Don't Repeat Yourself).\n"
    "4. Recommend using standard template libraries (STL) with better performance or more efficient data structures, while keeping the overall algorithm the same. Do not suggest any modifications to the algorithm.\n"
    "5. Do not make suggestions related to comments.\n"
    "6. Suggestions should focus on enhancing readability and maintainability without compromising the functionality of the code. If the suggestion is subjective and not a necessity, do not deduct points from the cleanliness score.\n"
    "7. Refactoring suggestions should not include code. Instead, clear and detailed instructions should be provided.\n"
    "8. Deduct cleanliness score by 1-5 points each time a refactoring suggestion is added, with minor issues deducting 1-3 points, and significant issues deducting up to 5 points. However, no points should be deducted for subjective suggestions. The score range is 0 <= score <= 100.\n"
    "9. Refactoring suggestions should only be based on the general principles of writing neat, efficient, and maintainable algorithm problem-solving code. Do not provide algorithmic suggestions.\n"
    "10. Rather than pointing out flaws, focus on how the user can improve and make suggestions as constructive as possible.\n"
    "11. Consolidate similar suggestions into one.\n"
    "12. Keep clean code principles such as the Single Responsibility Principle (SRP), Don't Repeat Yourself (DRY), and Keep It Simple, Stupid (KISS) in mind when suggesting.\n"
    "13. Maintain a balance of suggestions between readability, performance improvement, and complexity reduction.\n"
    "14. Do not discuss modifications to the algorithm. Only make suggestions for creating cleaner code.\n"
    "15. Do not make suggestions related to comments.\n"
    "16. Remember that the code input is a portion of the code. If the beginning and end of the code seem awkward, it's because only a middle portion of the code is being shown.\n"
    "RESPONSE FORMAT:\n"
    "--------\n"
    "gpt_solution_refactoring_suggestion: <Suggestions for refactoring the user's code (numbered list, replace commas with spaces, be as detailed as possible)>,\n"
    "gpt_solution_clean_score: <Cleanliness score of user's code (Only number)>,\n"
    "--------\n"
)

SUMMARY_CODE_REFACTORING = PromptTemplate(
    input_variables=["problem_info", "user_code"],
    template=SUMMARY_CODE_REFACTORING_TMPL,
)