import json
import re

def parse_questions_answers(file_path):
    questions_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        
        # Adjusted regex to specifically match questions with exactly four options A, B, C, D and exclude E
        pattern = r'(\d+)\s*(.*?)\s*A\.\s*(.*?)\s*B\.\s*(.*?)\s*C\.\s*(.*?)\s*D\.\s*(.*?)\s*Answer:\s*([A-D]).*?\s*(Explanation:\s*(.*))?'
        
        questions = content.split('Question:')
        for question in questions[1:]:  # Skip the first split as it's not a question
            match = re.search(pattern, question, re.DOTALL)
            if match:
                question_number = match.group(1)
                question_text = match.group(2).strip()
                options = {
                    'A': match.group(3).strip(),
                    'B': match.group(4).strip(),
                    'C': match.group(5).strip(),
                    'D': match.group(6).strip(),
                }
                answer = match.group(7)
                explanation = match.group(9).strip() if match.group(9) else ""
                
                # Construct the question-answer-options structure
                questions_dict[f'Question {question_number}'] = {
                    'question': question_text,
                    'options': options,
                    'answer': answer,
                    'explanation': explanation
                }

    return questions_dict

def save_to_json(data, file_path='questions_answers2.json'):
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

# Replace 'cdl.txt' with your actual file path
file_path = 'set2.txt'  # Update this path to the actual file path
questions_answers = parse_questions_answers(file_path)
save_to_json(questions_answers)
