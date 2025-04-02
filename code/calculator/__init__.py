from config import *
from sympy import *

def calculate(node):
    value = 0
    if isinstance(node,dict) and len(node):
        child = node['structure']
        if node['type']==NODE_TYPE['e']:
            t = calculate(child[0])
            if len(child)>1:
                type,e_pi = calculate(child[1])
                if type:
                    return t-e_pi
                return t+e_pi
            return t
        elif node['type']==NODE_TYPE['e_pi']:
            if len(child)>0:
                t = calculate(child[1])
                type,e_pi = calculate(child[2])
                if type == 0:
                    result = t+e_pi
                else:
                    result = t-e_pi
                if child[0]=='-':
                    return 1,result
                return 0,result
            else:
                return 0,0
        elif node['type']==NODE_TYPE['t']:
            f = calculate(child[0])
            if len(child)>1:
                type,t_pi = calculate(child[1])
                if type == 0:
                    return f*t_pi
                else:
                    return f/t_pi
            return f
        elif node['type']==NODE_TYPE['t_pi']:
            if len(child)>0:
                f = calculate(child[1])
                type,t_pi = calculate(child[2])
                if type==0:
                    result = f*t_pi
                else:
                    result = f/t_pi
                if child[0] == 'div':
                    return 1,result
                return 0,result
            else:
                return 0,1
        elif node['type']==NODE_TYPE['bracket']:
            return calculate(child[1])
        elif node['type'] == NODE_TYPE['integer']:
            return int(child)
        elif node['type'] == NODE_TYPE['decimal']:
            return float(child)
    return value

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')
variable_table = {'x':x,'y':y,'z':z}

forward_step = 1

def set_forward_step(steps):
    global forward_step
    forward_step = steps
def simplify_node(node):
    global forward_step

    if node['status'] == STATUS['solved'] and forward_step > 0:
        forward_step = forward_step - 1
        node['structure'] = node['value']

def post_order(node):
    global variable_table,forward_step
    latex_str = ''
    if isinstance(node, dict) and len(node):
        child  = node['structure']
        if node['type'] == NODE_TYPE['constant']:
            print('post_order constant')
            node['status'] = STATUS['solved']
            if node['structure'] == 'pi':
                node['value'] = pi
            elif node['structure'] == 'e':
                node['value'] = E
            latex_str = latex(node['value'])
        elif node['type'] == NODE_TYPE['integer'] or node['type'] == NODE_TYPE['decimal']:
            # print('post_order integer|decimal')
            node['status'] = STATUS['solved']
            # node['attribute'] = ATTRIBUTE['constant']
            if node['type'] == NODE_TYPE['integer']:
                node['value'] = int(node['structure'])
            else:
                node['value'] = float(node['structure'])
            latex_str = str(node['value'])
        elif node['type'] == NODE_TYPE['variable']:
            # print('post_order variable')
            node['status'] = STATUS['poly1']
            # node['attribute'] = ATTRIBUTE['variable']

            if node['structure'] in variable_table:
                # print('coefficient:',node['coefficient'])
                if isinstance(node['coefficient'],int):
                    node['coefficient'] = int(node['coefficient'])
                if isinstance(node['coefficient'],float):
                    node['coefficient'] = float(node['coefficient'])
                node['value'] = int(node['coefficient'])*variable_table[node['structure']]
                # print(node['value'])
            # node['value'] = str(node['coefficient'])+'*'+node['structure']
            else:
                raise (ValueError,'post_order variable:unrecognized variable')
            # print('coefficient=',node['coefficient'])
            if node['coefficient'] == 1:
                latex_str = node['structure']
            elif node['coefficient'] == -1:
                latex_str = '-'+node['structure']
            else:
                # print('yessss')
                # print(type(node['coefficient']))
                latex_str = str(node['coefficient'])+node['structure']
        elif not isinstance(node['structure'],list):
            return str(node['structure'])
        elif node['type'] == NODE_TYPE['bracket']:
            # print('post_order bracket',child)
            in_bracket = post_order(child[1])
            node['status'] = child[1]['status']
            # node['attribute'] = child[1]['attribute']
            if node['status'] in [ STATUS['poly1'] , STATUS['poly2'],STATUS['other']]:
                node['value'] = (child[1]['value'])
            elif node['status'] == STATUS['solved']:
                node['value'] = child[1]['value']
            else:
                raise(ValueError,'post_order:unresolved node status')
            latex_str = '('+in_bracket+')'
        elif node['type'] == NODE_TYPE['t_pi']:
            # print('post_order t_pi')
            if len(child)==2:
                f = post_order(child[1])
                node['status'] = child[1]['status']
                node['value'] = child[1]['value']
                if child[0] == 'times':
                    node['flag'] = 0
                    latex_str = '\\times'+f
                elif child[0] == 'div':
                    node['flag'] = 1
                    latex_str = '\\div'+f
            elif len(child)>2:
                f = post_order(child[1])
                t_pi = post_order(child[2])
                node['status'] = max(child[1]['status'],child[2]['status'])
                if child[2]['flag'] == 1:
                    node['flag'] = 1
                    if node['status']== STATUS['solved']:
                        if child[1]['value']%child[2]['value']==0:
                            node['value'] = int(child[1]['value']/(child[2]['value']))
                        else:
                            node['value'] = child[1]['value'] / (child[2]['value'])
                    elif node['status'] == STATUS['poly1'] or node['status'] == STATUS['poly2']:
                        node['value'] = child[1]['value']/child[2]['value']
                    else:
                        raise (ValueError,'post_order:t_pi')
                    latex_str = '\\times'+f+t_pi
                else:
                    node['flag'] = 0
                    if node['status']== STATUS['solved']:
                        node['value'] = child[1]['value']*(child[2]['value'])
                    elif node['status'] == STATUS['poly1'] or node['status'] == STATUS['poly2']:
                        node['value'] = child[1]['value']*(child[2]['value'])
                    else:
                        raise (ValueError,'post_order:t_pi')
                    latex_str = '\\div' + f + t_pi
                simplify_node(node)
            else:
                node['status'] = STATUS['solved']
                node['value'] = 1
                node['flag'] = 0
            # print(node['value'])
        elif node['type']==NODE_TYPE['t']:
            # print('post_order t',child[0])
            f = post_order(child[0])
            node['status'] = child[0]['status']
            node['value'] = child[0]['value']
            latex_str = f
            if len(child)>1:
                t_pi = post_order(child[1])
                latex_str = latex_str  + t_pi
                node['status'] = max(child[0]['status'],child[1]['status'])
                if child[1]['flag'] == 1:

                    if node['status'] == STATUS['solved']:
                        if child[0]['value']%child[1]['value']==0:
                            node['value'] = int(child[0]['value']/(child[1]['value']))
                        else:
                            node['value'] = child[0]['value'] / (child[1]['value'])
                    elif node['status'] == STATUS['poly1'] or node['status'] == STATUS['poly2']:
                        node['value'] = child[0]['value']/child[1]['value']
                    else:
                        raise (ValueError,'post_order:t')
                else:

                    if node['status']== STATUS['solved']:
                        node['value'] = child[0]['value']*(child[1]['value'])
                    elif node['status'] in VARIABLE_STATUS:
                        node['value'] = child[0]['value']*child[1]['value']
                    else:
                        raise (ValueError,'post_order:t')
                simplify_node(node)
        elif node['type']==NODE_TYPE['e_pi']:
            # print('post_order e_pi')
            # print('post_order e_pi:',node)
            if len(child) == 2:
                t = post_order(child[1])
                latex_str = child[0]+t
                node['status'] = child[1]['status']
                if child[0] == '+':
                    node['value'] = child[1]['value']
                    node['flag'] = 0
                else:
                    node['value'] = -child[1]['value']
                    node['flag'] = 1
            elif len(child)>2:
                t = post_order(child[1])
                e_pi = post_order(child[2])
                latex_str = child[0] + t + e_pi

                node['status'] = max(child[1]['status'],child[2]['status'])
                if child[0] == '-':
                    child[1]['value'] = -child[1]['value']
                if child[2]['flag'] == 0:
                    if node['status'] == STATUS['solved']:
                        node['value'] = child[1]['value']+child[2]['value']
                    elif node['status'] == STATUS['poly1'] or node['status'] == STATUS['poly2']:
                        node['value'] = child[1]['value'] + child[2]['value']
                    else:
                        raise (ValueError,'post_order:e_pi')
                else:
                    if node['status'] == STATUS['solved']:
                        node['value'] = child[1]['value']+child[2]['value']
                    elif node['status'] == STATUS['poly1'] or node['status'] == STATUS['poly2']:
                        node['value'] = child[1]['value'] + child[2]['value']
                    else:
                        raise (ValueError,'post_order:e_pi')
                if child[0]=='-':
                    node['flag'] = 1
                else:
                    node['flag'] = 0
                simplify_node(node)
            else:
                node['structure'] = 0
                node['status'] = STATUS['solved']
                node['value'] = 0
                node['flag'] = 0
            # print(node['value'])
        elif node['type'] == NODE_TYPE['e']:
            # print('post_order e')
            t = post_order(child[0])
            node['status'] = child[0]['status']
            node['value'] = child[0]['value']
            latex_str = t
            if len(child) > 1:
                e_pi = post_order(child[1])
                latex_str = latex_str + e_pi
                node['status'] = max(child[0]['status'], child[1]['status'])
                # if child[1]['value'] == 3:
                # print('child1',child[1])
                if child[1]['flag'] == 1:
                    if node['status'] == STATUS['solved']:
                        node['value'] = child[0]['value'] + child[1]['value']
                    elif node['status'] == STATUS['poly1'] or node['status'] == STATUS['poly2']:
                        node['value'] = child[0]['value'] + child[1]['value']
                    else:
                        raise (ValueError, 'post_order:e')
                else:
                    if node['status'] == STATUS['solved']:
                        node['value'] = child[0]['value'] + child[1]['value']
                    elif node['status'] in VARIABLE_STATUS:
                        node['value'] = child[0]['value'] + child[1]['value']
                    else:
                        raise (ValueError, 'post_order:t_pi')
                simplify_node(node)

    return latex_str

def solve_expression(parser_tree):
    global x
    post_order(parser_tree)
    if parser_tree['type'] == NODE_TYPE['equation']:
        child = parser_tree['structure']
        # print(child[0]['value'],child[1]['value'])
        return solve(Eq(child[0]['value'],child[1]['value']),x)
    else:
        return parser_tree['value']