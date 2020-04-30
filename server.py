from flask import Flask, request, redirect, render_template, url_for
import data_manager
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def main_page():
    file_data = data_manager.get_latest_questions()
    return render_template('main_page.html', data=file_data)


@app.route("/list")
def all_questions():
    questions = data_manager.get_data_by_table('question')
    ordered_direction = "desc"
    ordered_by = "submission_time"
    args = request.args
    if "ordered_direction" in args and "ordered_by" in args:
        ordered_direction = args.get('ordered_direction')
        ordered_by = args.get('ordered_by')
    if ordered_direction == "desc":
        try:
            questions = sorted(questions, key=lambda k: int(k[ordered_by]), reverse=True)
        except:
            questions = sorted(questions, key=lambda k: k[ordered_by], reverse=True)
    elif ordered_direction == "asc":
        try:
            questions = sorted(questions, key=lambda k: int(k[ordered_by]))
        except:
            questions = sorted(questions, key=lambda k: k[ordered_by])

    return render_template("all_questions.html", questions=questions,
                           ordered_direction=ordered_direction, ordered_by=ordered_by)


@app.route('/question/<question_id>',  methods=['GET','POST'])
def question(question_id):
    if request.method == 'POST':
        tag=request.form.get('add_tag')
        try:
            data_manager.update_question_tags(question_id, tag)
        except:
            return redirect('/question/'+str(question_id)+'/new-tag')
    comment_id_answer = data_manager.get_data_by_table('comment')
    comment_id_question = data_manager.get_data_by_id('comment', 'question_id', question_id)
    file_data = data_manager.get_data_by_id('question', 'id', question_id)[0]
    new = file_data.get('view_number', '') + 1
    data_manager.update_number('question', 'view_number', new, question_id)
    answers = data_manager.get_data_by_id('answer', 'question_id', question_id)
    tags = data_manager.tags(question_id)
    return render_template('question.html', id=question_id, data=file_data, answers=answers,
                           comment_id_question=comment_id_question, comment_id_answer=comment_id_answer, tags=tags)


@app.route('/question/<question_id>/new-comment', methods=['POST','GET'])
def new_comment(question_id):
    if request.method == 'POST':
        question_id = question_id
        message = request.form.get('add-comment')
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        edited_count = 0
        data_manager.write_comment(question_id, message, submission_time, edited_count)
        return redirect('/question/' + str(question_id))
    return render_template('new-comment.html', id=question_id)


@app.route('/question/<question_id>/new_answer', methods=["GET", "POST"])
def post_new_answer(question_id):
    if request.method == 'POST':
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        vote_number = 0
        question_id = question_id
        message = request.form.get('message')
        image = request.form.get('image')
        data_manager.write_answer(submission_time, vote_number, question_id, message, image)
        return redirect('/question/' + str(question_id))
    return render_template('new_answer.html', id=question_id)


@app.route("/question/<question_id>/vote_up")
def Q_vote_up(question_id):
    file_data=data_manager.get_data_by_id('question', 'id', question_id)[0]
    new=file_data.get('vote_number', '') + 1
    data_manager.update_number('question', 'vote_number', new,question_id)
    return redirect('/list')


@app.route("/question/<question_id>/vote_down")
def Q_vote_down(question_id):
    file_data=data_manager.get_data_by_id('question', 'id', question_id)[0]
    new=file_data.get('vote_number', '') - 1
    data_manager.update_number('question', 'vote_number', new,question_id)
    return redirect('/list')


@app.route("/answer/<answer_id>/vote_up")
def A_vote_up(answer_id):
    file_data = data_manager.get_data_by_id('answer', 'id', answer_id)[0]
    new = file_data.get('vote_number', '') + 1
    question_id = file_data.get('question_id','')
    data_manager.update_number('answer', 'vote_number', new, answer_id)
    question_data=data_manager.get_data_by_id('question', 'id', question_id)[0]
    new_view=question_data.get('view_number', '') - 1
    data_manager.update_number('question', 'view_number', new_view, question_id)
    return redirect('/question/'+ str(question_id))


@app.route("/answer/<answer_id>/vote_down")
def A_vote_down(answer_id):
    file_data = data_manager.get_data_by_id('answer', 'id', answer_id)[0]
    new = file_data.get('vote_number', '') - 1
    question_id = file_data.get('question_id', '')
    data_manager.update_number('answer', 'vote_number', new, answer_id)
    question_data=data_manager.get_data_by_id('question', 'id', question_id)[0]
    new_view=question_data.get('view_number', '') - 1
    data_manager.update_number('question', 'view_number', new_view, question_id)
    return redirect('/question/' + str(question_id))


@app.route('/add_question', methods=["GET", "POST"])
def add_question():
    if request.method == 'POST':
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        view_number = 0
        vote_number = 0
        title = request.form.get('title')
        message = request.form.get('message')
        image = request.form.get('image')
        data_manager.write_question(submission_time, view_number, vote_number, title, message, image)
        return redirect("/list")
    return render_template("add_question.html")


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    data_manager.delete_from_table_by_id('question', question_id)
    return redirect("/list")


@app.route('/question/<question_id>/edit', methods=["GET", "POST"])
def edit_question(question_id):
    file_data=data_manager.get_data_by_id('question', 'id', question_id)[0]
    if request.method == 'POST':
        data_manager.update_data('question', 'title', request.form.get('title'), question_id)
        data_manager.update_data('question', 'message', request.form.get('message'), question_id)
        data_manager.update_data('question', 'image', request.form.get('image'), question_id)
        return redirect('/list')
    return render_template('edit.html', id=question_id, data=file_data)


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    file_data = data_manager.get_data_by_id('answer', 'id', answer_id)[0]
    question_id = file_data.get('question_id', '')
    data_manager.delete_from_table_by_id('answer', answer_id)
    return redirect("/question/" + str(question_id))


@app.route('/search')
def search():
    phrase = request.args.get('search_text')
    search_text = data_manager.search(phrase)
    return render_template('search.html', search_text=search_text, phrase=phrase)



@app.route("/answer/<answer_id>/new-comment", methods=['POST', 'GET'])
def new_comment_answer(answer_id):
    if request.method == 'POST':
        message = request.form.get('comment-answer')
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        edited_count = 0
        data_manager.comment_answer(answer_id, message, submission_time, edited_count)
        file_data = data_manager.get_data_by_id('answer', 'id', answer_id)[0]
        question_id = file_data.get('question_id', '')
        return redirect('/question/' + str(question_id))
    return render_template('comment-answer.html', id=answer_id)


@app.route("/question/<question_id>/new-tag", methods=['GET','POST'])
def add_tags(question_id):
    tags = data_manager.get_all_tags()
    if request.method == 'POST':
        if request.form.get('new_tag'):
            new_tag = request.form.get('new_tag')
            data_manager.add_new_tag(new_tag)
            return redirect('/question/'+str(question_id)+'/new-tag')
    return render_template('add_tags.html', question_id=question_id, tags=tags)


@app.route("/question/<question_id>/tag/<tag_id>/delete")
def delete_tag(question_id, tag_id):
    data_manager.delete_tag(question_id, tag_id)
    return redirect('/question/'+str(question_id))


@app.route("/comment/<comment_id>/edit", methods=['POST', 'GET'])
def edit_comment(comment_id):
    file_data = data_manager.get_data_by_id('comment', 'id', comment_id)[0]
    question_id = file_data.get('question_id', '')
    if question_id is None:
        answer_id=file_data.get('answer_id', '')
        data2 = data_manager.get_data_by_id('answer', 'id', answer_id)[0]
        question_id=data2.get('question_id', '')
    if request.method == 'POST':
        data=data_manager.get_edit_number(comment_id)[0]
        value=data.get('edited_count','')
        data_manager.update_edit_number(value, comment_id)
        data_manager.update_data('comment', 'message', request.form.get('edit-comment-answer'), comment_id)
        return redirect('/question/' + str(question_id))
    return render_template('edit_comment.html', comment_id=comment_id, data=file_data)



@app.route("/comment/<comment_id>/delete", methods=['POST', 'GET'])
def delete_comment(comment_id):
    data = data_manager.get_data_by_id('comment', 'id', comment_id)[0]
    question_id=data.get('question_id','')
    if question_id is None:
        answer_id=data.get('answer_id','')
        data2 = data_manager.get_data_by_id('answer', 'id', answer_id)[0]
        question_id = data2.get('question_id', '')
    data_manager.delete_comment(comment_id)
    return redirect('/question/' + str(question_id))




if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
