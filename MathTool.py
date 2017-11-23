import urllib.request as request
import urllib.parse as parse
import json, math
from itertools import permutations as perm

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
    func = {1: solve_polynomial, 2:integrate, 3: differentiate, 4: eigen, 5:rk4, 6: integer_partition, 7: sequence, 8: series_sum, 9: permute}
    choice = int(input("Choice: "))
    return func[choice]()

def make_json(func_string):
    #print(base_url + parse.urlencode([('input', func_string), ('format', 'plaintext'), ('output', 'JSON'), ('appid', key)]))
    return json.loads(request.urlopen(base_url + parse.urlencode([('input', func_string), ('format', 'plaintext'), ('output', 'JSON'), ('appid', key)])).read().decode(encoding='utf-8'))

def solve_polynomial():
    func = input("Enter polynomial: ")
    if '=' not in func:
        func += ' = 0'
    json_data = make_json(func)
    hub = json_data['queryresult']['pods']
    factors = hub[1]['subpods'][0]['plaintext'].split('=')[0]
    if len(factors) == 0:
        factors = hub[2]['subpods'][0]['plaintext'].split('=')[0]
    rs = ''
    for i in hub[3]['subpods']:
        if '=' in i['plaintext']:
            rs += i['plaintext'].split('x = ')[1] + ", "
        else:
            rs += i['plaintext'].split('x~')[1] + ", "
    cs = ''
    for i in hub[4]['subpods']:
        if len(i['plaintext']) == 0:
            cs += "None  "
            break
        elif '=' in i['plaintext']:
            cs += i['plaintext'].split('x = ')[1] + ", "
        else:
            cs += i['plaintext'].split('x~')[1] + ", "
    return 'Factors: {f}\nReal Solution: {{{rs}}}\nComplex Solution: {cs}'.format(f=factors,rs=rs[:-2],cs=cs[:-2])

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
    num = "integer partition of " + input("Enter number to find partitions of: ")
    return 'Number of partitions = {}'.format(make_json(num)['queryresult']['pods'][2]['subpods'][0]['plaintext'])

def sequence():
    notfound = '(no form found in terms of holonomic sequences)'
    series = input("Enter first few numbers of the series (separated by comma): ") + ",..."
    data = make_json(series)['queryresult']['pods']
    if data[-1]['subpods'][0]['plaintext'] == notfound:
        return "No match found"
    else:
        return data[1]['subpods'][0]['plaintext'] + '\n' + data[1]['infos']['text'] + "\nURL: " + data[1]['infos']['links'][0]['url']

def series_sum():
    series = input("Enter first few terms of the series (comma separated): ").replace(',','+')
    last = input("Enter last term after for finite sum or blank to calculate infinite sum: ")
    if len(last) == 0:
        series += "+..."
    else:
        series += "+...+" + str(last)
    data = make_json(series)['queryresult']['pods']
    return "Sum = {}\nConvergence: {}".format(data[1]['subpods'][0]['plaintext'], data[2]['subpods'][0]['plaintext'])

def permute():
    data = input('Enter elements seperated by comma to permute: ').split(',')
    a = set()
    for i in perm(data):
        if i not in a:
            a.add(i)
    return '\n'.join(map(lambda x: str(x), a))

def display():
    result = get_function()
    print("----------\n" + result + "\n----------")

if __name__ == '__main__':
    while True:
        intro()
        display()
        if input("Quit? (y/n)").lower() == 'y':
            break
    print("Courtesy of Wolfram Alpha. Program intended for personal use only.")
