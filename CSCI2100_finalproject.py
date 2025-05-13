class Node:
    def __init__(self, value, id):
        self.value = value
        self.id = id
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None
    def height(self, node):
        if not node:
            return 0
        return node.height

    def balance(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)
    def insert(self, root, value, id):
        if not root:
            return Node(value, id)
        elif (value, id) < (root.value, root.id):
            root.left = self.insert(root.left, value, id)
        else:
            root.right = self.insert(root.right, value, id)
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance = self.balance(root)

        # left-rotation
        if balance > 1 and (value, id) < (root.left.value, root.left.id):
            return self.right_rotate(root)
        if balance < -1 and (value, id) > (root.right.value, root.right.id):
            return  self.left_rotate(root)
        if balance > 1 and (value, id) > (root.left.value, root.left.id):
           root.left = self.left_rotate(root.left)
           return self.right_rotate(root)
        if balance < -1 and (value, id) < (root.right.value, root.right.id):
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def delete(self, root, value, id):
        if not root:
            return root

        if (value, id) < (root.value, root.id):
            root.left = self.delete(root.left, value, id)
        elif (value, id) > (root.value, root.id):
            root.right = self.delete(root.right, value, id)
        else:
            if not root.left:
                temp = root.right
                root = None
                return temp
            elif not root.right:
                temp = root.left
                root = None
                return temp

            temp = self.min_value_node(root.right)
            root.value = temp.value
            root.id = temp.id
            root.right = self.delete(root.right, temp.value, temp.id)

        if not root:
            return root

        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance = self.balance(root)

        #left rotation
        if balance > 1 and self.balance(root.left) >= 0:
            return self.right_rotate(root)

        if balance < -1 and self.balance(root.right) <= 0:
            return self.left_rotate(root)
        if balance > 1 and self.balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and self.balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root.right)
        return root

    def left_rotate(self, z):
        y = z.right
        B = y.left

        y.left = z
        z.right = B

        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        return y

    def right_rotate(self, z):
        y = z.left
        B = y.right

        y.right = z
        z.left = B

        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        return y

    def search(self, root, value, id):
        if not root or (root.value == value and root.id == id):
            return root
        if (root.value, root.id) < (value, id):
            return self.search(root.right, value, id)
        return self.search(root.left, value, id)

    def query_range(self, root, price1, price2, listID):
        if not root:
            return
        if root.value >= price1:
            self.query_range(root.left, price1, price2, listID)
        if price1 <= root.value <= price2:
            listID.append(root.id)
        if root.value <= price2:
            self.query_range(root.right, price1, price2, listID)
        return listID

    def insert_value(self, value, id):
        self.root = self.insert(self.root, value, id)
    def delete_value(self, value, id):
        self.root = self.delete(self.root, value, id)
    def search_value(self, value, id):
        return self.search(self.root, value, id)
    def query_range_price(self, price1, price2):
        listID = []
        return self.query_range(self.root, price1, price2, listID)

    def min_value_node(self, root):
        current = root
        while current.left:
            current = current.left
        return current
    def max_value_node(self, root):
        current = root
        while current.right:
            current = current.right
        return current.value

class StockTracker:
    def __init__(self):
        self.stocksID = { }
        self.treePrice = AVLTree()
        self.treeVolume = AVLTree()

    def insert_new_stock(self, id, price):
        if id in self.stocksID:
            return
        self.stocksID[id] = {"price": price, "volume": 0}
        self.treePrice.insert_value(price, id)
        self.treeVolume.insert_value(0, id)


    def update_price(self, id, price):
        if id not in self.stocksID:
            return
        old_price = self.stocksID[id]["price"]
        if old_price == price:
            return
        self.treePrice.delete_value(old_price, id)
        self.treePrice.insert_value(price, id)
        self.stocksID[id]["price"] = price

    def lookup_by_id(self, id):
        if id not in self.stocksID:
            return None
        print(self.stocksID[id]["price"], self.stocksID[id]["volume"])
        return self.stocksID[id]["price"], self.stocksID[id]["volume"]

    def price_range(self, p1, p2):
        print(self.treePrice.query_range_price(p1, p2))
        return self.treePrice.query_range_price(p1, p2)

    def increase_volume(self, id, volume_increase):
        if id not in self.stocksID:
            return
        old_vol = self.stocksID[id]["volume"]
        vol_incr = self.stocksID[id]["volume"] + volume_increase
        self.treeVolume.delete_value(old_vol, id) #logn time
        self.treeVolume.insert_value(vol_incr, id) #logn time
        self.stocksID[id]["volume"] = vol_incr

    def max_vol(self):
        print(self.treeVolume.max_value_node(self.treeVolume.root))
        return self.treeVolume.max_value_node(self.treeVolume.root) #logn time

if __name__ == "__main__":
    tracker = StockTracker()
    count = 0
    #the project works based on the file "stocks_test"
    with open('stocks_test.txt', 'r') as file:

        for line in file:
            operation = line.strip() #remove new line characters
            count += 1 #to count how many operations we have done

            try:
                if operation.startswith("insert_new_stock"):
                    args = operation[len("insert_new_stock("):-1].split(',') #extract the arguments from the operation
                    tracker.insert_new_stock(int(args[0]), float(args[1]))
                elif operation.startswith("update_price"):
                    args = operation[len("update_price("):-1].split(',')
                    tracker.update_price(int(args[0]), float(args[1]))
                elif operation.startswith("increase_volume"):
                    args = operation[len("increase_volume("):-1].split(',')
                    tracker.increase_volume(int(args[0]), int(args[1]))
                elif operation.startswith("price_range"):
                    args = operation[len("price_range("):-1].split(',')
                    result = tracker.price_range(float(args[0]), float(args[1]))
                elif operation == "max_vol()":
                    result = tracker.max_vol()
                elif operation.startswith("lookup_by_id"):
                    stock_id = int(operation[len("lookup_by_id("):-1])
                    result = tracker.lookup_by_id(stock_id)
            except Exception as e: #exception handling
                print(f"Error executing operation {count}: {operation}")
                print(f"Error: {str(e)}")

    print("Successfully executed, yay :)")













