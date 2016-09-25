/**
 * Created by anton on 9/22/16.
 */
public class MarkingTree {
    private Node[] tree;
    private int size;
    public int numberOfMarked;
    private boolean[] markedNodes;

    public MarkingTree(int size) {
        numberOfMarked = 0;
        this.size = size;
        tree = new Node[size+1];
        markedNodes = new boolean[size+1];
        for (int i = 1; i <= size; i++) { //node numbering 1..N
            tree[i] = new Node(i);
            markedNodes[i] = false;
        }
    }

    public boolean[] markedNodes() {
        return markedNodes;
    }


    public void markNode(int id) {  //mark node and cascade
        Node node = tree[id];
        //numberOfMarked++;
        node.mark();
        cascade(id);
    }

    private void cascade(int id) {
        int parentId     = (id) / 2;
        int leftChildId  = 2 * id;
        int rightChildId = 2 * id + 1;

        Node parent = tree[parentId];   // current node's parent
        Node sibling = null;                // current node's sibling

        if (id % 2 == 0) {  // left child
            sibling = tree[2 * parentId + 1];
        } else {            // right child
            sibling = tree[2 * parentId];
        }

        Node rightChild, leftChild = null;
        Node me = tree[id];

        if ((2 * id) < size) { // any children inside tree?
            leftChild  = tree[leftChildId];
            rightChild = tree[rightChildId];

            if (me.marked && leftChild.marked && !rightChild.marked) {
                rightChild.mark();
                //numberOfMarked++;
                cascade(rightChildId);
            } else if (me.marked && rightChild.marked && !leftChild.marked) {
                leftChild.mark();
                //numberOfMarked++;
                cascade(leftChildId);
            }
        }

        if (id != 1) { //not at root
            if (me.marked && sibling.marked && !parent.marked) {
                //numberOfMarked++;
                parent.mark();
                cascade(parentId);
            }
            if (me.marked && !sibling.marked && parent.marked) {
                //numberOfMarked++;
                sibling.mark();
                cascade(sibling.index);
            }
        }
    }


    public class Node {
        public boolean marked;
        public int index;

        public Node(int index) {
            this.index = index;
            marked = false;
        }

        public void mark() {
            if (marked != true) {
                //System.out.println("Marked: " + index);
                marked = true;
                numberOfMarked++;
                markedNodes[index] = true;
            }
            //marked = true;
        }
    }

}
