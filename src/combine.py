from pandas import DataFrame, read_csv


def main():
    experiments = ["B", "C", "D"]
    for experiment in experiments:
        submission_input, resubmission_input, select, submission_output, resubmission_output, submission_vicki, resubmission_vicki = get_files(
            experiment)

        data = get_maps(resubmission_input, resubmission_output, select, submission_input, submission_output, experiment,
                        submission_vicki, resubmission_vicki)

        info = {"sis_id": [], "selected_ai_grading": [], "submission": [], "submission_ai_score": [],
                "submission_ai_comment": [], "resubmission": [], "resubmission_ai_score": [],
                "resubmission_ai_comment": [], "question1": [], "question2": [], "question3": [], "question4": [],
                "question5": [], "question6": [], "question7": [], "submission_vicki_comment": [], "submission_vicki_score": [], "resubmission_vicki_comment": [], "resubmission_vicki_score": []}

        process_data(info, data)

        save_data(info, data, experiment)


def get_files(experiment):
    submission_input = read_csv(
        f"../Data/{experiment}/Recursion_Practice_{experiment}1_Quiz_Student_Analysis_Report_clean.csv",
        encoding="ISO-8859-1")
    resubmission_input = read_csv(
        f"../Data/{experiment}/Recursion_Practice_{experiment}2_Revisited_Survey_Student_Analysis_Report_clean.csv",
        encoding="ISO-8859-1")
    select = read_csv("../Data/S24_Select_clean.csv", encoding="ISO-8859-1")
    submission_output = read_csv(f"../Data/{experiment}/S24_AI_Feedback_{experiment}1_experiment_0.csv",
                                 encoding="ISO-8859-1")
    resubmission_output = read_csv(f"../Data/{experiment}/S24_AI_Feedback_{experiment}2_experiment_0.csv",
                                   encoding="ISO-8859-1")
    submission_vicki = read_csv(f"../Data/{experiment}/Vicki_Comments_{experiment}1.csv", encoding="ISO-8859-1")
    resubmission_vicki = read_csv(f"../Data/{experiment}/Vicki_Comments_{experiment}2.csv", encoding="ISO-8859-1")
    return submission_input, resubmission_input, select, submission_output, resubmission_output, submission_vicki, resubmission_vicki


def get_maps(resubmission_input, resubmission_output, select, submission_input, submission_output, experiment,
             submission_vicki, resubmission_vicki):
    output_resubmission_ai_prompt = resubmission_output["ai_starting_prompt"].to_list()
    output_resubmission_problem = resubmission_output[f"problem{experiment}2"].to_list()
    output_resubmission_example_solutions = resubmission_output["solution"].to_list()
    output_resubmission_example_student_codes = resubmission_output["studentCode"].to_list()
    output_resubmission_example_comments = resubmission_output["comment"].to_list()

    question1_answers = resubmission_input["How useful was the feedback"].to_list()
    question2_answers = resubmission_input["What aspects of the feedback are useful? "].to_list()
    question3_answers = resubmission_input["What could make the feedback more useful?"].to_list()
    question4_answers = resubmission_input[
        "How long did it take you to understand the feedback and rewrite the solution? "].to_list()
    question5_answers = resubmission_input["I understand recursion,"].to_list()
    question6_answers = resubmission_input["I can follow the execution of a recursive function."].to_list()
    question7_answers = resubmission_input["I can write a recursive function"].to_list()

    submission_vicki_sis_ids = submission_vicki["sisUserId"].to_list()
    submission_vicki_comments = submission_vicki["submissionComment"].to_list()
    submission_vicki_scores = submission_vicki["submissionScore"].to_list()

    sis_id_to_submission_vicki_comment = get_map(submission_vicki_sis_ids, submission_vicki_comments)
    sis_id_to_submission_vicki_score = get_map(submission_vicki_sis_ids, submission_vicki_scores)

    resubmission_vicki_sis_ids = resubmission_vicki["sisUserId"].to_list()
    resubmission_vicki_comments = resubmission_vicki["resubmissionComment"].to_list()
    resubmission_vicki_scores = resubmission_vicki["resubmissionScore"].to_list()

    sis_id_to_resubmission_vicki_comment = get_map(resubmission_vicki_sis_ids, resubmission_vicki_comments)
    sis_id_to_resubmission_vicki_score = get_map(resubmission_vicki_sis_ids, resubmission_vicki_scores)

    submission_data = get_submission_maps(submission_input, submission_output)

    resubmission_data = get_submission_maps(resubmission_input, resubmission_output)

    select_sis_ids = select["SIS User ID"].to_list()
    select_indicators = select["indicator"].to_list()

    sis_id_to_indicator = get_map(select_sis_ids, select_indicators)

    input_resubmission_sis_ids = resubmission_input["sis_id"].to_list()

    sis_id_to_question1_answers = get_map(input_resubmission_sis_ids, question1_answers)
    sis_id_to_question2_answers = get_map(input_resubmission_sis_ids, question2_answers)
    sis_id_to_question3_answers = get_map(input_resubmission_sis_ids, question3_answers)
    sis_id_to_question4_answers = get_map(input_resubmission_sis_ids, question4_answers)
    sis_id_to_question5_answers = get_map(input_resubmission_sis_ids, question5_answers)
    sis_id_to_question6_answers = get_map(input_resubmission_sis_ids, question6_answers)
    sis_id_to_question7_answers = get_map(input_resubmission_sis_ids, question7_answers)

    data = {
        "output_resubmission_ai_prompt": output_resubmission_ai_prompt,
        "output_resubmission_problem": output_resubmission_problem,
        "output_resubmission_example_solutions": output_resubmission_example_solutions,
        "output_resubmission_example_student_codes": output_resubmission_example_student_codes,
        "output_resubmission_example_comments": output_resubmission_example_comments,
        "submission_data": submission_data,
        "resubmission_data": resubmission_data,
        "sis_id_to_indicator": sis_id_to_indicator,
        "sis_id_to_submission_vicki_comment": sis_id_to_submission_vicki_comment,
        "sis_id_to_submission_vicki_score": sis_id_to_submission_vicki_score,
        "sis_id_to_resubmission_vicki_comment": sis_id_to_resubmission_vicki_comment,
        "sis_id_to_resubmission_vicki_score": sis_id_to_resubmission_vicki_score,
        "sis_id_to_question1_answers": sis_id_to_question1_answers,
        "sis_id_to_question2_answers": sis_id_to_question2_answers,
        "sis_id_to_question3_answers": sis_id_to_question3_answers,
        "sis_id_to_question4_answers": sis_id_to_question4_answers,
        "sis_id_to_question5_answers": sis_id_to_question5_answers,
        "sis_id_to_question6_answers": sis_id_to_question6_answers,
        "sis_id_to_question7_answers": sis_id_to_question7_answers
    }

    return data


def get_submission_maps(submission_input, submission_output):
    input_submission_sis_ids = submission_input["sis_id"].to_list()
    input_submission_prompts = submission_input["prompt"].to_list()

    output_submission_prompts = submission_output["Student Input"].to_list()
    output_submission_ai_scores = submission_output["AI Score"].to_list()
    output_submission_ai_evaluations = submission_output["AI Evaluation"].to_list()

    input_ids = get_ids(input_submission_prompts)
    output_ids = get_ids(output_submission_prompts)
    if set(input_ids) != set(output_ids):
        raise ValueError("The ids are not the same from the input and output files")

    sis_id_to_submission_id = get_map(input_submission_sis_ids, input_ids)
    submission_id_to_submission = get_map(output_ids, output_submission_prompts)
    submission_id_to_submission_ai_score = get_map(output_ids, output_submission_ai_scores)
    submission_id_to_submission_ai_evaluation = get_map(output_ids, output_submission_ai_evaluations)

    data = {
        "sis_id_to_submission_id": sis_id_to_submission_id,
        "submission_id_to_submission": submission_id_to_submission,
        "submission_id_to_submission_ai_score": submission_id_to_submission_ai_score,
        "submission_id_to_submission_ai_evaluation": submission_id_to_submission_ai_evaluation
    }

    return data


def get_map(list1, list2):
    return dict(zip(list1, list2))


def get_ids(prompts):
    ids = []
    for prompt in prompts:
        try:
            ids.append(hash(prompt.replace("Â", "").replace(" ", "").strip()))
        except AttributeError:
            print(f"weird prompt: {prompt}")
    return ids


def clean_string(string):
    return string.replace("Â", " ").strip()


def process_data(info, data):
    for sis_id, indicator in data["sis_id_to_indicator"].items():
        try:
            submission_id = data["submission_data"]["sis_id_to_submission_id"][sis_id]
            submission = data["submission_data"]["submission_id_to_submission"][submission_id]
            submission_ai_score = data["submission_data"]["submission_id_to_submission_ai_score"][submission_id]
            submission_ai_evaluation = data["submission_data"]["submission_id_to_submission_ai_evaluation"][
                submission_id]
        except KeyError:
            submission = ""
            submission_ai_score = ""
            submission_ai_evaluation = ""

        try:
            resubmission_id = data["resubmission_data"]["sis_id_to_submission_id"][sis_id]
            resubmission = data["resubmission_data"]["submission_id_to_submission"][resubmission_id]
            resubmission_ai_score = data["resubmission_data"]["submission_id_to_submission_ai_score"][resubmission_id]
            resubmission_ai_evaluation = data["resubmission_data"]["submission_id_to_submission_ai_evaluation"][
                resubmission_id]
        except KeyError:
            resubmission = ""
            resubmission_ai_score = ""
            resubmission_ai_evaluation = ""

        try:
            submission_vicki_comment = data["sis_id_to_submission_vicki_comment"][sis_id]
            submission_vicki_score = data["sis_id_to_submission_vicki_score"][sis_id]
        except KeyError:
            submission_vicki_comment = ""
            submission_vicki_score = ""

        try:
            resubmission_vicki_comment = data["sis_id_to_resubmission_vicki_comment"][sis_id]
            resubmission_vicki_score = data["sis_id_to_resubmission_vicki_score"][sis_id]
        except KeyError:
            resubmission_vicki_comment = ""
            resubmission_vicki_score = ""

        try:
            question1 = data["sis_id_to_question1_answers"][sis_id]
            question2 = data["sis_id_to_question2_answers"][sis_id]
            question3 = data["sis_id_to_question3_answers"][sis_id]
            question4 = data["sis_id_to_question4_answers"][sis_id]
            question5 = data["sis_id_to_question5_answers"][sis_id]
            question6 = data["sis_id_to_question6_answers"][sis_id]
            question7 = data["sis_id_to_question7_answers"][sis_id]
        except KeyError:
            question1 = ""
            question2 = ""
            question3 = ""
            question4 = ""
            question5 = ""
            question6 = ""
            question7 = ""

        info["sis_id"].append(sis_id)
        info["selected_ai_grading"].append(indicator)
        info["submission"].append(clean_string(submission))
        info["submission_ai_score"].append(submission_ai_score)
        info["submission_ai_comment"].append(submission_ai_evaluation)
        info["resubmission"].append(clean_string(resubmission))
        info["resubmission_ai_score"].append(resubmission_ai_score)
        info["resubmission_ai_comment"].append(resubmission_ai_evaluation)
        info["question1"].append(question1)
        info["question2"].append(question2)
        info["question3"].append(question3)
        info["question4"].append(question4)
        info["question5"].append(question5)
        info["question6"].append(question6)
        info["question7"].append(question7)
        info["submission_vicki_comment"].append(submission_vicki_comment)
        info["submission_vicki_score"].append(submission_vicki_score)
        info["resubmission_vicki_comment"].append(resubmission_vicki_comment)
        info["resubmission_vicki_score"].append(resubmission_vicki_score)


def blank_column(size):
    return ["" for _ in range(size)]


def get_column(lst, size):
    if len(lst) < size:
        return lst + blank_column(size - len(lst))
    return lst


def get_max_list_length(info):
    return max(len(lst) for lst in info.values())


def save_data(info, data, experiment):
    max_list_length = get_max_list_length(info)
    scoring = DataFrame()
    scoring["AI Starting Prompt"] = get_column(data["output_resubmission_ai_prompt"], max_list_length)
    scoring["Problem"] = get_column(data["output_resubmission_problem"], max_list_length)
    scoring["Solutions"] = get_column(data["output_resubmission_example_solutions"], max_list_length)
    scoring["Example Student Code"] = get_column(data["output_resubmission_example_student_codes"], max_list_length)
    scoring["Example Comment on Example Student code"] = get_column(data["output_resubmission_example_comments"], max_list_length)
    scoring[""] = blank_column(max_list_length)
    scoring[""] = blank_column(max_list_length)
    scoring["Student sis_id"] = get_column(info["sis_id"], max_list_length)
    scoring["Selected for AI grading"] = get_column(info["selected_ai_grading"], max_list_length)
    scoring["Student Submission Input"] = get_column(info["submission"], max_list_length)
    scoring["AI Score Submission"] = get_column(info["submission_ai_score"], max_list_length)
    scoring["AI Feedback Submission"] = get_column(info["submission_ai_comment"], max_list_length)
    scoring["Vicki Score Submission"] = get_column(info["submission_vicki_score"], max_list_length)
    scoring["Vicki Feedback Submission"] = get_column(info["submission_vicki_comment"], max_list_length)
    scoring["How useful was the feedback"] = get_column(info["question1"], max_list_length)
    scoring["What aspects of the feedback are useful?"] = get_column(info["question2"], max_list_length)
    scoring["What could make the feedback more useful?"] = get_column(info["question3"], max_list_length)
    scoring["How long did it take you to understand the feedback and rewrite the solution?"] = get_column(info["question4"], max_list_length)
    scoring["I understand recursion,"] = get_column(info["question5"], max_list_length)
    scoring["I can follow the execution of a recursive function."] = get_column(info["question6"], max_list_length)
    scoring["I can write a recursive function"] = get_column(info["question7"], max_list_length)
    scoring["Student Resubmission Input"] = get_column(info["resubmission"], max_list_length)
    scoring["AI Score Resubmission"] = get_column(info["resubmission_ai_score"], max_list_length)
    scoring["AI Feedback Resubmission"] = get_column(info["resubmission_ai_comment"], max_list_length)
    scoring["Vicki Score Resubmission"] = get_column(info["resubmission_vicki_score"], max_list_length)
    scoring["Vicki Feedback Resubmission"] = get_column(info["resubmission_vicki_comment"], max_list_length)
    scoring["submission accuracy: How accurate/good is the submission? 1-5"] = blank_column(max_list_length)
    scoring["resubmission accuracy: How accurate/good is the resubmission? 1-5"] = blank_column(max_list_length)
    scoring["apply_feedback: Does the student appropriately apply the feedback? For example, when the feedback says “Check for nulls”, does the student understand that and apply it in their resubmission?: Yes/Partial/No"] = blank_column(max_list_length)
    scoring["prop_errors: What proportion of key errors in the student’s original submission does the feedback capture? None/Marginally/Half/Most/All"] = blank_column(max_list_length)
    scoring["prop_feedback: What proportion of errors does the student fix, based on the feedback? For example, if the feedback tells student to do step A, but also hints at steps B and C, is student able to also do steps B and C? None/Marginally/Half/Most/All"] = blank_column(max_list_length)
    scoring["add_incorrect: Does student add things that are incorrect to the resubmission? Yes/No"] = blank_column(max_list_length)
    scoring["feedback_incorrect: Does the feedback contain any suggestions or hints that are incorrect or irrelevant? Yes/Partial/No"] = blank_column(max_list_length)
    scoring["disregard: If feedback is incorrect, is the student able to disregard the feedback? Yes/Partial/No"] = blank_column(max_list_length)
    scoring["notes: Open-ended notes (your thoughts on the submission and your scoring)"] = blank_column(max_list_length)
    scoring.to_csv(f"../{experiment}1_{experiment}2_scoring.csv")


if __name__ == "__main__":
    main()
