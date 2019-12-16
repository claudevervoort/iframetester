from flask import Flask, request, make_response, render_template
app = Flask(__name__)

def inc_cookie(resp, key, val, samesite):
    val = int(val) + 1 if val else 1
    # This version of werkzeug does not contain the fix to handle None so going manual
    # resp.set_cookie(key, str(val), samesite=samesite)
    samesite_str = f';SameSite={samesite}' if samesite else ''
    resp.headers.add('Set-Cookie', f"{key}={str(val)}{samesite_str}")
    
@app.route('/')
def cookie_business():
    lax_mode = request.cookies.get('lax_mode')
    none_mode = request.cookies.get('none_mode')
    not_set = request.cookies.get('not_set')
    cookies = {
        'none': none_mode if none_mode else 'not set, setting it',
        'lax': lax_mode if lax_mode else 'not set, setting it',
        'not_set': not_set if not_set else 'not set, setting it'
    }
    resp = make_response( render_template ('cookies.html', cookies = cookies ) )
    inc_cookie(resp, 'none_mode', none_mode, 'None')
    inc_cookie(resp, 'not_set', not_set, None)
    inc_cookie(resp, 'lax_mode', lax_mode, 'Lax')
    return resp

if __name__ == '__main__':
    app.run()