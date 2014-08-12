from flask import Flask, render_template, request, url_for
import smtplib, urllib, urllib2

# Initialize the Flask application
app = Flask("pyText")

# Define a route for the default URL, which loads the form
@app.route('/')
def form():
    return render_template('form_submit.html')

# Define a route for the action of the form, for example '/hello/'
# We are also defining which type of requests this route is 
# accepting: POST requests in this case
@app.route('/send/', methods=['POST', 'GET'])
def send():
	error = None
    # name=request.form['yourname']
    # email=request.form['youremail']
	gmail_address = request.form['gmail_address']
	gmail_password = request.form['gmail_password']
	phone_number = request.form['phone_number']
	message = request.form['message']
	provider = ''
	url = 'http://www.txt2day.com/lookup.php'
	values = {'action' : 'lookup',
	           'pre' : phone_number[0:3],
	           'ex' : phone_number[3:6],
	           'myButton' : 'Find Provider'}
	data = urllib.urlencode(values)  ##provider checker
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	the_page = response.read()
	if 'Boost' in the_page:
	    provider = '@myboostmobile.com'
	if 'Rogers' in the_page:
	    provider = '@pcs.rogers.com'
	if 'Sprint' in the_page:
	    provider = '@pm.sprint.com'
	if 'Tmobile' in the_page:
	    provider = '@tmomail.net'
	if 'Virgin Mobile' in the_page:
	    provider = '@vmobl.com'
	if 'Verizon' in the_page:
	    provider = '@vzwpix.com'
	if 'Att' in the_page:
	    provider = '@mms.att.net'
	if 'unknown' in the_page:
	    provider = "Failed To Identify Provider"
	    return render_template('form_action.html')
	    exit

	if 'unknown' not in the_page:
		server = smtplib.SMTP( "smtp.gmail.com", 587 )
		server.starttls()
		server.login( gmail_address, gmail_password )
		server.sendmail( phone_number, phone_number + provider, message )
		server.quit()

		return render_template('form_action.html', provider=provider)
	else:
		error = 'Invalid username/password'
		return render_template('form_submit.html', error=error)

if __name__ == '__main__':
  app.run(debug=False)
