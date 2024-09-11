
import os

def factorize(f,var):
    if(var.islower()):
        comp_var = var.capitalize()
        
    else:
        comp_var = var.lower()

    minterms = f.split("+")
    result = []

    for item in minterms:
        if var in item:
            item = item.replace(var,'')

        elif comp_var in item:
            continue
        
        item = item.replace(" ","")
        result.append(item)
    return set(result)  
    

def main():
    
    os.system("clear")
    
    Welcome_text = """
    
    Python script to obtain Cofactor for given Boolean equation wrt given cube
    
    
    The script is written using few assumptions : 
    1. Normal variables are represented using lower case variables (a,b,x,y)
    2. Complement variables are represented using Upper case variables (A,B,X,Y)
    
    Upon start of script, the user is expected to input the Boolean expression(seperated by (+) and without spaces).
    Ex : Ab+Cd+abD
    
    Next, user is expcted to input the cube for which the cofactor for given boolean expression must be computed
    
    After successful inputs, the program returns the cofactor
    
    """
    
    print(Welcome_text)
    
    f = input("    Enter the Function: ")
    cube = input("    Enter the cube: ")

    for literal in cube:
        f = '+'.join(list(factorize(f,literal)))
    print("    Co-factor function : ",f)

if __name__ == "__main__":
    main()