from flask import Flask, request, make_response, render_template
app = Flask(__name__)

def inc_cookie(resp, key, val, samesite):
    val = int(val) + 1 if val else 1
    # This version of werkzeug does not contain the fix to handle None so going manual
    # resp.set_cookie(key, str(val), samesite=samesite)
    samesite_str = f';SameSite={samesite}' if samesite else ''
    resp.headers.add('Set-Cookie', f"{key}={str(val)}{samesite_str};Path=/;Secure;HttpOnly")
    
@app.route('/')
def welcome():
    return make_response( render_template ('welcome.html' ) )

@app.route('/page/<pagename>')
def cookie_business(pagename):
    resp = make_response( render_template ('cookies.html', cookies = request.cookies.items() ) )
    for k, v in request.cookies.items():
        if not pagename in k and '_SameSite_' in k:
            inc_cookie(resp, k, v, 'Lax' if 'Lax' in k else 'None')
    none_cookie_name = f'{pagename}_SameSite_None'
    lax_cookie_name = f'{pagename}_SameSite_Lax'
    inc_cookie(resp, none_cookie_name, request.cookies[none_cookie_name] if none_cookie_name in request.cookies else 0, 'None')
    inc_cookie(resp, lax_cookie_name, request.cookies[lax_cookie_name] if lax_cookie_name in request.cookies else 0, 'Lax')
    return resp

if __name__ == '__main__':
    app.run()