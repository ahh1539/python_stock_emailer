import smtplib
import email.message
import yfinance as yf
from health_screen_script import automate_health_checkin
from datetime import datetime, timedelta
from yahoo_fin import stock_info as si


def login_email(email, password):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Connect to the server
        server.starttls()  # Use TLS
        server.login(email, password)  # Login to the email server
        print("login success")
        return server
    except smtplib.SMTPException:
        print('login error')
        exit()



def send_email(recipient, emaill, server, stock_data):
    try:
        msg = email.message.Message()
        msg['Subject'] = "Your Daily Stock Analysis for: {}".format(datetime.today().strftime('%Y-%m-%d'))
        msg['From'] = 'alex-stock-bot'
        msg['To'] = recipient
        msg.add_header('Content-Type','text/html')
        msg.set_payload(stock_data)

        # message = 'Subject: {}\n\n{}'.format("Your Daily Stock Analysis for: {}".format(
        #     datetime.today().strftime('%Y-%m-%d')), stock_data)
        server.sendmail(emaill, recipient, msg.as_string())  # Send the email
        print('Success: Sent to {}'.format(recipient))
    except smtplib.SMTPException:
        print("Error: Unable to send email")


def get_stock_data(tickers):
    yesterday = datetime.now() - timedelta(days=1)
    all_stock_defriefs = '<h1>Here is your daily stock analysis: </h1></br>'
    for ticker in tickers:
        try:
            # get data on this ticker
            tickerData = yf.Ticker(ticker)

            # get the historical prices for this ticker
            # tickerDf = tickerData.history(
            #     period='1d', start=yesterday, end=yesterday)
            # see your data

            stock_debrief = '<h4>' + str(tickerData.info.get('shortName')).strip().capitalize() + '</h2></br>'
            stock_debrief += '<ul><li><h4>Current Price: {}</h4></li></ul><hr>'.format(float("{:.2f}".format(si.get_live_price(ticker))))
            # stock_debrief += '<p>{}</p><hr>'.format(si.get_financials(ticker, yearly = True, quarterly = True))
            all_stock_defriefs += stock_debrief
            print(all_stock_defriefs)
        except:
            print('error occured with ticker: {}'.format(ticker))
    return all_stock_defriefs


def main():
    email_server = login_email('*******@gmail.com', '*********')
    tickers = ['MSFT', 'TQQQ', 'SPXL', 'NTDOY', 'TCEHY', 'AMD', 'AAPL']

    daily_debreif = get_stock_data(tickers)
    send_email('******', '********',
               email_server, daily_debreif)



if __name__ == "__main__":
    main()
