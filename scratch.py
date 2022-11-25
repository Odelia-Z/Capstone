if __name__ == "__main__":
    
    d = {}
    
    if not any(item in ['age', 'name'] for item in list(d.keys())):
        print(False)