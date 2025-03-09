from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Simulating a database for tickets
tickets = [
    {"id": 1, "event": "Music Concert", "price": 100, "available": 10},
    {"id": 2, "event": "Movie Premiere", "price": 50, "available": 20},
    {"id": 3, "event": "Theater Play", "price": 80, "available": 15},
]

# Home route
@app.route('/')
def index():
    return render_template('index.html', tickets=tickets)

# Book ticket route
@app.route('/book/<int:ticket_id>', methods=['GET', 'POST'])
def book_ticket(ticket_id):
    ticket = next((t for t in tickets if t['id'] == ticket_id), None)
    if not ticket:
        flash("Ticket not found!", "error")
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Get the number of tickets the user wants to book
        num_tickets = int(request.form['num_tickets'])
        if num_tickets > ticket['available']:
            flash(f"Sorry, only {ticket['available']} tickets are available.", "error")
        else:
            # Update the ticket availability
            ticket['available'] -= num_tickets
            flash(f"Successfully booked {num_tickets} tickets for {ticket['event']}!", "success")
            return redirect(url_for('confirmation', ticket=ticket, num_tickets=num_tickets))

    return render_template('book_ticket.html', ticket=ticket)

# Confirmation route
@app.route('/confirmation')
def confirmation():
    ticket_id = request.args.get('ticket_id')
    num_tickets = request.args.get('num_tickets')
    ticket = next((t for t in tickets if t['id'] == int(ticket_id)), None)
    if ticket:
        return render_template('confirmation.html', ticket=ticket, num_tickets=num_tickets)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
