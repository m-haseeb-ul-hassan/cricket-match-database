
def parse_id(mid):
    # parse the match id into PSL , league , match 
    try:
        league , num = mid.rsplit("-" , 1)
        i = len (league) - 1
        while i >= 0 and league[i].isdigit():
            i -= 1
        lname = league[:i+1]
        lnum = int(league[i+1:]) if i < len(league)-1 else 0
        return (lname , lnum , int(num) )
    except:
        return  (mid, 0 , 0)


# node for player BST 
class PNode:
    def __init__(self , name ):
        self.name = name 
        self.left = None 
        self.right = None 
        self.ht = 1  # height of Avl
        
        
        
        
# AVL for players inside each matches      
class PlayerBST:
    def __init__(self):
        self.root = None 
        
    def _ht(self, n):
        return 0 if n == None else n.ht
        
    def _fix (self, n):
        # update height and rotate if tree unbalanced 
        n.ht = 1+ max(self._ht(n.left), self._ht(n.right))
        bf = self._ht(n.left) - self._ht(n.right)
        
        if bf > 1:
            if self._ht(n.left.left) < self._ht(n.left.right):
                n.left = self._rot_l(n.left)      # left right case
            return self._rot_r(n)
        
        if bf < -1:
            if self._ht(n.right.right) < self._ht(n.right.left):
                n.right = self._rot_r(n.right)     # right left case
            return self._rot_l(n)
        return n
    
    def _rot_r(self, y):
        x = y.left
        y.left = x.right 
        x.right = y
        y.ht = 1 + max(self._ht(y.left), self._ht(y.right) )
        x.ht = 1+ max(self._ht(x.left) , self._ht(x.right)) 
        return x
    
    def _rot_l(self , x):
        y = x.right 
        x.right = y.left
        y.left = x
        x.ht = 1 + max(self._ht(x.left) , self._ht(x.right) )
        y.ht = 1 + max (self._ht(y.left) , self._ht(y.right))
        return y 
    
    def _insert(self, n , name):
        if n == None:
            return PNode(name)
        if name < n.name:
            n.left = self._insert(n.left , name)
        elif name > n.name:
            n.right = self._insert(n.right , name)
        else:
            print (f" {name} is already in team.")
            return n 
        return self._fix(n)
    
    def add (self , name):
        self.root = self._insert (self.root , name)
    
    def _del(self, n, name):
        if n == None:
            return None, False 
        
        found = False 
        if name < n.name :
            n.left , found = self._del(n.left , name)
        elif name > n.name:
            n.right , found = self._del(n.right , name)
        else :
            found = True 
            if n.left == None:
                return n.right , found 
            if n.right == None: 
                return n.left , found
            
            # two children
            s = n.right 
            while s.left != None:
                s = s.left
            n.name = s.name 
            n.right, _ = self._del (n.right , s.name)
        if n != None:
            n = self._fix(n)
        return n , found 
    
    def remove (self, name):
        self.root , found = self._del(self.root , name)
        if not found:
            print (f" {name} not found in the team.")
        return found 
    
    def _inorder(self , n , res):
        if n == None :
            return 
        self._inorder (n.left , res)
        res.append (n.name)
        self._inorder (n.right , res)
        
    def to_list (self):
        res = []
        self._inorder (self.root , res)
        return res
    
    def display(self):
        names = self.to_list()
        if len(names) == 0:
            print (" No Player found.")
            return 
        for n in names:
            print (f" {n}")
            
# match record       
class Match :
    def __init__(self, mid , t1, t2, date , winner , loc):
        self.mid = mid 
        self.t1 = t1
        self.t2 = t2
        self.date = date
        self.winner = winner
        self.loc = loc 
        self.t1_players = PlayerBST()  # each match has ots own player bst
        self.t2_players = PlayerBST()
        
    def __str__(self):
        t1 = self.t1_players.to_list()
        t2 = self.t2_players.to_list()
        t1_str = "\n  ".join(t1) if t1 else "No players found."
        t2_str = "\n  ".join(t2) if t2 else "No Players found."
        return (f"\n Match ID: {self.mid}\nDate: {self.date}\n"
                f"Location: {self.loc}\nWinner: {self.winner}\n"
                f"{self.t1}:\n  {t1_str}\n"
                f"{self.t2}:\n    {t2_str}\n")   
        
# node for match 
class MNode:
    def __init__(self, match):
        self.match = match 
        self.left = None 
        self.right = None 
        self.ht = 1
    
# matches bst 

class CricketDatabase:
    def __init__(self):
        self.root = None 
    
    def _ht(self, n):
        return 0 if n == None else n.ht
    
    def _fix(self , n):
        n.ht = 1+ max(self._ht(n.left), self._ht(n.right) )
        bf = self._ht(n.left ) - self._ht(n.right)
        
        if bf > 1:
            if self._ht (n.left.left) < self._ht(n.left.right):
                n.left = self._rot_l(n.left)
            return self._rot_r(n)
        
        if bf < -1:
            if self._ht(n.right.right) < self._ht(n.right.left):
                n.right = self._rot_r(n.right)
            return self._rot_l(n)
        return n 
        
    def _rot_r(self , y):
        x = y.left
        y.left = x.right 
        x.right = y
        y.ht = 1 + max(self._ht(y.left) , self._ht(y.right) )
        x.ht = 1+ max(self._ht(x.left) , self._ht(x.right))
        return x
    
    def _rot_l(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        x.ht = 1 + max(self._ht(x.left) , self._ht(x.right))
        y.ht = 1 + max(self._ht(y.left) , self._ht(y.right))
        return y 
    
    def _insert(self, n , match):
        if n == None:
            return MNode(match)
        if parse_id(match.mid) < parse_id(n.match.mid):
            n.left = self._insert(n.left , match)
        elif parse_id(match.mid) > parse_id(n.match.mid):
            n.right = self._insert(n.right , match)
        else:
            print(f"Match {match.mid} already exist!!!")
            return n 
        return self._fix(n)
    
    def add_match(self, match):
        self.root = self._insert(self.root , match)
    
    def _find(self, n , mid):
        if n == None:
            return None 
        if n.match.mid == mid:
            return n.match 
        if parse_id(mid) < parse_id(n.match.mid):
            return self._find(n.left , mid)
        return self._find(n.right , mid)
    
    def find_match(self, mid):
        return self._find (self.root , mid)
    
    def _del(self , n , mid):
        if n == None:
            return None , False
        found = False
        
        if parse_id(mid) < parse_id (n.match.mid):
            n.left , found = self._del(n.left, mid)
        elif parse_id(mid) > parse_id(n.match.mid):
            n.right , found = self._del(n.right , mid)
        else:
            found = True
            if n.left == None:
                return n.right , found 
            if n.right == None:
                return n.left , found
            s = n.right 
            while s.left != None:
                s = s.left
            n.match = s.match
            n.right, _ = self._del(n.right , s.match.mid)
             
        if n != None:
            n = self._fix(n)
        return n , found
    
    def delete_match(self, mid):
        self.root , found = self._del(self.root , mid)
        if found:
            print(f" Match {mid} deleted.")
        else:
            print(f" Match {mid} not found.")
        return found 
    
    def _inorder(self, n):
        if n == None:
            return 
        self._inorder(n.left)
        print(n.match)
        self._inorder(n.right)
        
    def print_matches(self):
        if self.root == None:
            print ("No Matches in database.")
            return 
        self._inorder(self.root)
        
    def add_cricketer(self, mid, team, name):
        m = self.find_match(mid)
        if m == None:
            print (f"Match {mid} not found.")
            return 
        if team == 1:
            m.t1_players.add(name)
        else:
            m.t2_players.add(name)
        
    def delete_circketer(self, mid , team , name):
        m = self.find_match(mid)
        if m == None:
            print (f" Match {mid} not found.")
            return False
        if team == 1:
            return m.t1_players.remove(name)
        return m.t2_players.remove(name)
    
    def _collect(self, n , lst):
        if n == None:
            return 
        self._collect(n.left , lst)
        lst.append(n.match)
        self._collect(n.right , lst)
        
    def find_matches_by_player(self, name):
        result = CricketDatabase()
        all_m = []
        
        self._collect(self.root , all_m)
        for m in all_m:
            if name in m.t1_players.to_list() or name in m.t2_players.to_list():
                copy = Match(m.mid , m.t1 , m.t2 , m.date , m.winner, m.loc)
                copy.t1_players = m.t1_players
                copy.t2_players = m.t2_players
                result.add_match(copy)
        return result
    
    
    def isBSTBalanced(self):
        def check(n):
            if n == None:
                return True , 0 
            lb , lh = check(n.left)    # check left BST 
            rb , rh = check(n.right)           # chek right bst
            bal = lb and rb and abs(lh - rh) <= 1 
            return bal , 1 + max (lh, rh )
        result , _ = check(self.root)
        print("Tree is balanced." if result else "Tree isn't balacned.")
        return result 
    
    def balanceTree(self):
        lst = []
        self._collect(self.root , lst)
        def build(lo, hi):
            if lo > hi:
                return None
            mid = (lo + hi)// 2
            n = MNode(lst[mid])
            n.left = build(lo, mid - 1)
            n.right = build(mid + 1 , hi)
            n.ht = 1 + max(self._ht(n.left) , self._ht(n.right))
            return n 
        
        self.root = build(0 , len(lst) - 1)
        print("Tree Balanced.")
        
    def save_to_file(self, filename):
        lst = []
        self._collect(self.root , lst)
        with open(filename , "w") as f:
            for m in lst:
                t1 = ",".join(m.t1_players.to_list())
                t2 = ",".join(m.t2_players.to_list())
                f.write(f"MATCH|{m.mid}|{m.t1}|{m.t2}|{m.date}|{m.winner}|{m.loc}\n")
                f.write(f"T1|{t1}\nT2|{t2}\nEND\n")
        print(f"Saved to {filename}.")
        
    def load_from_file(self, filename):
        try:
            f = open(filename , "r")
        except FileNotFoundError:
            print("File not found, strting New!")
            return 
        self.root = None 
        cur = None 
        for line in f:
            line = line.strip()
            if line.startswith("MATCH|"):
                p = line.split("|")
                cur = Match(p[1], p[2], p[3], p[4], p[5], p[6])
            elif line.startswith("T1|") and cur != None:
                for p in line[3:].split(","):
                    if p: cur.t1_players.add(p)
            
            elif line.startswith("T2|") and cur != None:
                for p in line[3:].split(","):
                    if p: cur.t2_players.add(p)
            elif line == "END" and cur != None:
                self.add_match(cur)
                cur = None 
        f.close()
        print(f"Loaded form {filename}.")
    
if __name__ == "__main__":
    db = CricketDatabase()
    db.load_from_file("matches.txt")
    
    while True:
        print("\n Welcome to Circket Match Database :)")
        print("1. Add Match\n2. Delete Match\n3. Find Match\n4. Print All Matches\n5. Add Cricketer\n6. Delete Cricketer\n7. Find Matches by Cricketer\n8. Is Balanced BST\n9. Balance Tree\n10. Save and Exit")
        ch = input("Enter choice:").strip()
        
        if ch == "1":
            mid = input("Match ID (like PSL1-1):").strip()
            t1 = input("Team 1:").strip()
            t2 = input("Team 2:").strip()
            d = input("Date:").strip()
            w = input("Winner:").strip()
            loc = input("Location:").strip()
            db.add_match( Match(mid , t1, t2 , d, w , loc))
        
        elif ch == "2":
            db.delete_match(input ("Match ID to delete:").strip())
            
        elif ch == "3":
            mid = input("Match ID to find:").strip()
            m = db.find_match(mid)
            print (m if m != None else f" Match {mid} not found.")
        
        elif ch == "4":
            db.print_matches()
        
        elif ch == "5":
            mid = input("Match ID:").strip()
            t = input ("Team (1 or 2):").strip()
            name = input("Cricketer name:").strip()
            db.add_cricketer(mid , int(t), name)
        
        elif ch == "6":
            mid = input("Match ID:").strip()
            t = input ("Team (1 or 2):").strip()
            name = input("Cricketer name:").strip()
            if db.delete_circketer(mid , int(t) , name):
                print(f"{name} removed.")
        
        elif ch == "7":
            name = input("Cricketer name:").strip()
            res = db.find_matches_by_player(name)
            if res.root == None:
                print(f"No Matches found for {name}.")
            else:
                print(f"\nMatches whre {name} played:")
                res.print_matches()
                
        elif ch == "8":
            db.isBSTBalanced()
            
        elif ch == "9":
            db.balanceTree()
        
        elif ch == "10":
            db.save_to_file("Matches.txt")
            print("Bye!")
            break
        
        else:
            print("Invalid choice.")                    

                
            
            
            
                 
























