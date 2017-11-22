import urllib.request as request
import urllib.parse as parse
import json, math

key = "WK3WR6-H56GY5954K"
base_url = "https://api.wolframalpha.com/v2/query?"

def intro():
    print("\n<OPERATIONS>"
          "\n 1) Factoring and Solutions to a Polynomial"
          "\n 2) Integrate <func> <OPTIONAL<lowerLimit, upperLimit>>"
          "\n 3) Differentiate <func> <OPTIONAL<lowerLimit, upperLimit>>"
          "\n 4) Eigenvalues and Eigenvectors of a matrix {{row1},{row2},...}"
          "\n 5) Runge-Kutta method, dy/dx = <func>, y(0) = <initial value>, from <start> to <end>, h = <step-size>"
          "\n 6) Integer Partition of an integer"
          "\n 7) Identifying the sequence and possibly, its formula"
          "\n 8) Sum of an infinite series"
          "\n 9) Permutation of a list")

def get_function():
    func = {1: solve_polynomial, 2:integrate, 3: differentiate, 4: eigen, 5:rk4, 6: integer_partition}
    choice = int(input("Choice: "))
    return func[choice]()

def make_json(func_string):
    return json.loads(request.urlopen(base_url + parse.urlencode([('input', func_string), ('format', 'plaintext'), ('output', 'JSON'), ('appid', key)])).read().decode(encoding='utf-8'))

def solve_polynomial():
    func = input("Enter polynomial: ")
    if '=' not in func:
        func += ' = 0'
    json_data = make_json(func)
    hub = json_data['queryresult']['pods']
    s = ''
    factors = hub[1]['subpods'][0]['plaintext'].split('=')[0]
    if len(factors) == 0:
        factors = hub[2]['subpods'][0]['plaintext'].split('=')[0]
    s += "Factors: " + factors + '\n'
    s += 'Real Solution: {'
    for i in hub[3]['subpods']:
        if '=' in i['plaintext']:
            s += i['plaintext'].split('x = ')[1] + ", "
        else:
            s += i['plaintext'].split('x~')[1] + ", "
    s = s[:-2] + "}\nComplex Solution: {"
    for i in hub[4]['subpods']:
        if len(i['plaintext']) == 0:
            s += "None  "
            break
        elif '=' in i['plaintext']:
            s += i['plaintext'].split('x = ')[1] + ", "
        else:
            s += i['plaintext'].split('x~')[1] + ", "
    s = s[:-2] + '}'
    return s

def integrate():
    func = "integrate " + input("f(x): ").rstrip()
    lim = input("Default is none; limits(comma separated): ").split(',')
    if len(lim) == 1:
        json_data = make_json(func)
    else:
        for i in range(len(lim)):
            if 'pi' in lim[i].lower():
                lim[i] = eval(lim[i].lower().replace('pi', str(math.pi)))
            else:
                lim[i] = int(lim[i])
        json_data = make_json(func + " " + str(tuple(lim)))
    return (json_data['queryresult']['pods'][0]['subpods'][0]['plaintext']).split('= ')[1]

def differentiate():
    func = "differentiate " + input("f(x): ").rstrip()
    return (make_json(func)['queryresult']['pods'][0]['subpods'][0]['plaintext']).split('= ')[1]

def eigen():
    func = "eigenvalues {" + input("Enter rows (enclosed within {}): ") + "}"
    data = make_json(func)
    eigenvalues = [i['plaintext'].split('= ')[1] for i in data['queryresult']['pods'][1]['subpods']]
    eigenvectors = [i['plaintext'].split('= ')[1] for i in data['queryresult']['pods'][2]['subpods']]
    pairs = tuple(zip(eigenvalues,eigenvectors))
    s = "Eigenvalue - EigenVector Pair:"
    for i in range(len(pairs)):
        s += '\n' + pairs[i][0] + ' --> ' + pairs[i][1]
    return s

def rk4():
    func = "Runge-Kutta method, dy/dx = " + input("dy/dx = ").rstrip()
    x0 = input("x0 = ")
    y0 = input("y0 = ")
    fr,to = tuple(map(lambda x: int(x), input("Enter range (comma, separated): ").split(',')))
    h = input("Step-size: ")
    string = '{}, y({}) = {}, from {} to {}, h = {}'.format(func, x0, y0, fr, to, h)
    data = make_json(string)['queryresult']['pods']
    result = data[2]['subpods'][0]['plaintext'].split('| ')[-3:]
    exact_soln = (data[6]['subpods'][0]['plaintext'])
    return 'x = {}\nExact Solution: {}\nLocal Error = {}\nGlobal Error = {}'.format(result[0],exact_soln,result[1],result[2])

def integer_partition():
    pass

def calculate():
    result = get_function()
    print("----------\n" + result + "\n----------")

if __name__ == '__main__':
    while True:
        intro()
        calculate()
        if input("Quit? (y/n)").lower() == 'y':
            break
    print("Courtesy of Wolfram Alpha. Program intended for personal use only.")
