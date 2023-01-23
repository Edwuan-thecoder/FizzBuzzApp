import sqlalchemy
from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required,  current_user
from .models import User, Records
from . import db

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # Very simple view func render template and passes the user info that is logged in.
    return render_template("home.html", user=current_user)


@views.route('/fizzbuzz', methods=['GET', 'POST'])
def fizzbuzz():
    # Our Fizz Buzz logic
    if request.method == 'POST':
        user_input = int(request.form['user_input'])
        fizz_string = ''
        if user_input % 3 == 0:
            fizz_string = 'Fizz'
        if user_input % 5 == 0:
            fizz_string += 'Buzz'
        if fizz_string == '':
            flash(f'{user_input} is neither Fizz OR Buzz.', category='error')
        else:
            flash(f'{fizz_string}', category='success')

        # record = db.engine.execute(f"SELECT * FROM Records WHERE user_inputs = '{user_input}'").first()
        record = Records.query.get(user_input)
        # Add/Update Record table depending on User input
        if record:

            print(record)
            print(record.amount_of_inputs)
            record.amount_of_inputs += 1
            db.session.commit()
        else:
            new_user_input = Records(user_inputs=user_input, amount_of_inputs=1)
            db.session.add(new_user_input)
            db.session.commit()
    return render_template('fizzbuzz.html', user=current_user)


@views.route('/top_records', methods=['GET', 'POST'])
def top_records():
    # Use SQLAlchemy ORM to retrieve all numbers used and the amount of times used
    all_inputs_in_order = Records.query.order_by(Records.amount_of_inputs.asc()).all()
    # print(max_inputs)
    empty_list = []
    for i in all_inputs_in_order:
        empty_list.append(i.amount_of_inputs)
    # sort through the records from greatest to least
    empty_list.sort(reverse=True)

    checker = True
    top_three_records = []
    index = 0
    # Logic to retrieve only the top three most common numbers used and amount of times used to store in a list to show User
    while checker:

        for i in all_inputs_in_order:
            if len(top_three_records) >= 3:
                checker = False
            if empty_list[index] == i.amount_of_inputs:
                top_three_records.append((i.user_inputs, i.amount_of_inputs))
        index += 1

    # Outputting end result
    first_record = f"The most common number is {top_three_records[0][0]} and it was submitted {top_three_records[0][1]} amount of times"
    second_record = f"The second most common number is {top_three_records[1][0]} and it was submitted {top_three_records[1][1]} amount of times"
    third_record = f"The third most common number is {top_three_records[2][0]} and it was submitted {top_three_records[2][1]} amount of times"
    records = [first_record, second_record, third_record]

    return render_template('top_records.html',  user=current_user, records=records)
