import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.Stack;

/**
 * Created by anton on 9/22/16.
 */
public class MarkingMain {
    int randomNotSeenIndex;
    private Stack<Integer> randomNotSeen;
    private Stack<Integer> randomNotMarked;
    Random r;
    MarkingTree tree;
    int size;
    int iterations = 100;

    public MarkingMain() {
        r = new Random();
        //initiateRandomStacks(size);

    }

    public List<Integer> R1(int size) {
        //System.out.println("Independent Random Select");
        this.size = size;
        ArrayList<Integer> roundResult = new ArrayList<Integer>();

        double average = 0;
        for (int i = 0; i < iterations; i++) {
            int rounds = 0;
            tree = new MarkingTree(size);
            while (tree.numberOfMarked < size) {
                rounds++;
                tree.markNode(independentRandomSelect(size));
            }
            roundResult.add(rounds);
            //System.out.println("Rounds: " + rounds);
        }
        return roundResult;
    }

    public List<Integer> R2(int size) {
        //System.out.println("Next Random Not Seen");
        this.size = size;
        ArrayList<Integer> roundResult = new ArrayList<Integer>();
        double average = 0;
        for (int i = 0; i < iterations; i++) {
            int rounds = 0;
            tree = new MarkingTree(size);
            initiateRandomStacks(size);
            while (tree.numberOfMarked < size) {
                rounds++;
                tree.markNode(nextRandomNotSeen());
            }
            roundResult.add(rounds);
            //System.out.println("Rounds: " + rounds);
        }
        return roundResult;
    }

    public List<Integer> R3(int size) {
        //System.out.println("Next Random Not Marked");
        this.size = size;
        ArrayList<Integer> roundResult = new ArrayList<Integer>();
        double average = 0;
        for (int i = 0; i < iterations; i++) {
            int rounds = 0;
            tree = new MarkingTree(size);
            initiateRandomStacks(size);
            while (tree.numberOfMarked < size) {
                rounds++;
                tree.markNode(nextRandomNotMarked());
            }
            roundResult.add(rounds);
            //System.out.println("Rounds: " + rounds);
        }
        return roundResult;
    }


    private int independentRandomSelect(int size) {
        int randomSelect = 1 + r.nextInt(size-1);
        return randomSelect;
    }

    private int nextRandomNotSeen() {
        return randomNotSeen.pop();
    }

    private int nextRandomNotMarked() {
        boolean[] markedNodes = tree.markedNodes();
        int nextIndex = randomNotMarked.pop();
        if (markedNodes[nextIndex] == false) {
            return nextIndex;
        } else {
            return nextRandomNotMarked();
        }
    }

    private void initiateRandomStacks(int size) {
        randomNotSeen = new Stack<Integer>();
        randomNotMarked    = new Stack<Integer>();

        int[] randomArray = new int[size]; // not using first index (1..N)
        for (int i = 0; i < size ; i++) randomArray[i] = i+1; // [1..size]

        //System.out.print("Random: ");
        //for (int i = 0; i < size ; i++) System.out.print(randomArray[i] + " ");

        randomArray = knuthShuffle(randomArray); //shuffle the order
        for (int i = randomArray.length -1; i >= 0; i--) {
            randomNotSeen.add(randomArray[i]);
        }

        //System.out.print("NotSeen: ");
        //for (int i = 0; i < size ; i++) System.out.print(randomArray[i] + " ");

        randomArray = knuthShuffle(randomArray); //shuffle the order
        for (int i = randomArray.length -1; i >= 0; i--) {
            randomNotMarked.add(randomArray[i]);
        }

        //System.out.print("NotMarked: ");
        //for (int i = 0; i < size ; i++) System.out.print(randomArray[i] + " ");

    }

    private int[] knuthShuffle(int[] inputDeck) {

        for (int i = 1; i <= inputDeck.length-1 ; i++) {
            int index = r.nextInt(i);
            // swap
            int tmp = inputDeck[index];
            inputDeck[index] = inputDeck[i];
            inputDeck[i] = tmp;
        }
        return inputDeck;
    }

    public static void main(String[] args) {
        int[] inputs = {3,7,15,31,63,127,255,511,1023,524287,1048575};
        //int[] inputs = {7};
        MarkingMain m = new MarkingMain();
        //m.initiateRandomStacks(size);
        for (int size: inputs) {
            System.out.printf("___________%nSize %d%n", size);
            System.out.print("Independent Random Select:\t");
            List<Integer> r = m.R1(size);
            double mean = mean(r);
            double sd = standardDeviation(r);
            System.out.printf("%.2f, %.2f.%n", mean, sd);

            System.out.print("Next Random Not Seen:\t\t");
            r = m.R2(size);
            mean = mean(r);
            sd = standardDeviation(r);
            System.out.printf("%.2f, %.2f.%n", mean, sd);

            System.out.print("Next Random Not Marked:\t\t");
            r = m.R3(size);
            mean = mean(r);
            sd = standardDeviation(r);
            System.out.printf("%.2f, %.2f.%n", mean, sd);

        }
    }

    public static double standardDeviation(List<Integer> a){
        int sum = 0;
        double mean = mean(a);
        for (Integer i : a)
            sum += Math.pow((i - mean), 2);
        return Math.sqrt( sum / ( a.size() - 1 ) ); // sample
    }

    public static double mean(List<Integer> a){
        int sum = sum(a);
        double mean = 0;
        mean = sum / (a.size() * 1.0);
        return mean;
    }

    public static int sum(List<Integer> a){
        if (a.size() > 0) {
            int sum = 0;
            for (Integer i : a) sum += i;
            return sum;
        }
        return 0;
    }

}