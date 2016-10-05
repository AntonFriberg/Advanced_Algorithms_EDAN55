import java.io.*;
import java.util.*;

/**
 * Created by Anton Friberg on 30/09/16.
 * Implementation of the Maximum Independent Set.
 */
public class IndependentSet {
    private int recursions;

    public static void main(String[] args) {
        IndependentSet s = new IndependentSet();
        s.run();
    }

    private void run() {
        String inputs[] = new String[]{"4", "30", "40", "50", "60", "70", "80", "90", "100", "110", "120", "130"};
        for (int i = 0; i < inputs.length; i++) {
            inputs[i] = "g" + inputs[i] + ".in";
            inputs[i] = addDataPath(inputs[i]);
        }

        System.out.printf("%-10s %10s %10s %20s%n", "file", "|V|", "alpha(G)", "recursive calls");
        for (int i = 0; i < 5; i++) {
            HashMap<Integer, List<Integer>> adjMatrix = loadData(inputs[i]);
            int size = adjMatrix.size();
            int result = algorithm_R_0(adjMatrix);
            System.out.printf("%-10s %10d %10d %20d%n", "g" + size + ".in", size, result, recursions);
        }

        recursions = 0;

        System.out.printf("%-10s %10s %10s %20s%n", "file", "|V|", "alpha(G)", "recursive calls");
        for (int i = 0; i < 9; i++) {
            HashMap<Integer, List<Integer>> adjMatrix = loadData(inputs[i]);
            int size = adjMatrix.size();
            int result = algorithm_R_1(adjMatrix);
            System.out.printf("%-10s %10d %10d %20d%n", "g" + size + ".in", size, result, recursions);
        }

        recursions = 0;

        System.out.printf("%-10s %10s %10s %20s%n", "file", "|V|", "alpha(G)", "recursive calls");
        for (int i = 0; i < 12; i++) {
            HashMap<Integer, List<Integer>> adjMatrix = loadData(inputs[i]);
            int size = adjMatrix.size();
            int result = algorithm_R_2(adjMatrix);
            System.out.printf("%-10s %10d %10d %20d%n", "g" + size + ".in", size, result, recursions);
        }

    }

    private int algorithm_R_0(HashMap<Integer, List<Integer>> adjMatrix) {
        recursions++;
        if (adjMatrix.isEmpty()) return 0;      // base case

        for (Integer i : adjMatrix.keySet()) {
            if (adjMatrix.get(i).isEmpty()) {   // if vertex without neighbor
                adjMatrix.remove(i);
                return (1 + algorithm_R_0(copy(adjMatrix)));
            }
        }

        int maximum = 0;
        int vertex = 0;
        for (Integer i : adjMatrix.keySet()) {
            if (adjMatrix.get(i).size() > maximum) {
                maximum = adjMatrix.get(i).size();      // maximum degree
                vertex = i;                             // vertex with maximum degree
            }
        }
        return Math.max(1+ algorithm_R_0(removeVAndNeighbors(adjMatrix, vertex)), algorithm_R_0(removeV(adjMatrix, vertex)));   // recursive call
    }

    private int algorithm_R_1(HashMap<Integer, List<Integer>> adjMatrix) {
        recursions++;
        if (adjMatrix.isEmpty()) return 0;      // base case

        for (Integer i : adjMatrix.keySet()) {  // exactly 1 neighbor
            if (adjMatrix.get(i).size() == 1) {
                return 1 + algorithm_R_1(removeVAndNeighbors(adjMatrix, i));
            }
        }

        for (Integer i : adjMatrix.keySet()) {
            if (adjMatrix.get(i).isEmpty()) {   // if vertex without neighbor
                adjMatrix.remove(i);
                return (1 + algorithm_R_1(copy(adjMatrix)));
            }
        }

        int maximum = 0;
        int vertex = 0;
        for (Integer i : adjMatrix.keySet()) {
            if (adjMatrix.get(i).size() > maximum) {
                maximum = adjMatrix.get(i).size();      // maximum degree
                vertex = i;                             // vertex with maximum degree
            }
        }
        return Math.max(1+ algorithm_R_1(removeVAndNeighbors(adjMatrix, vertex)), algorithm_R_1(removeV(adjMatrix, vertex)));   // recursive call
    }

    private int algorithm_R_2(HashMap<Integer, List<Integer>> adjMatrix) {
        recursions++;
        if (adjMatrix.isEmpty()) return 0;      // base case

        for (Integer i : adjMatrix.keySet()) {  // exactly 2 neighbor
            if (adjMatrix.get(i).size() == 2) {
                Integer neighbor1 = adjMatrix.get(i).get(0);
                Integer neighbor2 = adjMatrix.get(i).get(1);

                if (adjMatrix.get(neighbor1).contains(neighbor2)) {
                    return 1 + algorithm_R_2(removeVAndNeighbors(adjMatrix, i));
                } else {
                    return 1 + algorithm_R_2(removeVAndAddZ(adjMatrix, i));
                }
            }
        }

        for (Integer i : adjMatrix.keySet()) {  // exactly 1 neighbor
            if (adjMatrix.get(i).size() == 1) {
                return 1 + algorithm_R_2(removeVAndNeighbors(adjMatrix, i));
            }
        }

        for (Integer i : adjMatrix.keySet()) {
            if (adjMatrix.get(i).isEmpty()) {   // if vertex without neighbor
                adjMatrix.remove(i);
                return (1 + algorithm_R_2(adjMatrix));
            }
        }

        int maximum = 0;
        int vertex = 0;
        for (Integer i : adjMatrix.keySet()) {
            if (adjMatrix.get(i).size() > maximum) {
                maximum = adjMatrix.get(i).size();      // maximum degree
                vertex = i;                             // vertex with maximum degree
            }
        }
        return Math.max(1+ algorithm_R_2(removeVAndNeighbors(adjMatrix, vertex)), algorithm_R_2(removeV(adjMatrix, vertex)));   // recursive call
    }

    private HashMap<Integer,List<Integer>> removeVAndAddZ(HashMap<Integer, List<Integer>> adjMatrix, Integer vertex) {
        HashMap<Integer, List<Integer>> cloneMatrix = copy(adjMatrix);
        Integer n1 = adjMatrix.get(vertex).get(0);
        Integer n2 = adjMatrix.get(vertex).get(1);

        List<Integer> n1Neighbors = cloneMatrix.get(n1);
        List<Integer> n2Neighbors = cloneMatrix.get(n2);

        for (Integer n : n2Neighbors) {
            cloneMatrix.get(n).remove(n2);
            if (!cloneMatrix.get(n).contains(n1)) {
                cloneMatrix.get(n).add(n1);
                n1Neighbors.add(n);
            }
        }
        cloneMatrix.remove(vertex);
        cloneMatrix.remove(n2);
        cloneMatrix.get(n1).remove(vertex);
        return cloneMatrix;
    }

    private HashMap<Integer, List<Integer>> removeVAndNeighbors(HashMap<Integer, List<Integer>> adjMatrix, Integer vertex) {
        HashMap<Integer, List<Integer>> cloneMatrix = copy(adjMatrix);
        List<Integer> neighborhood = new ArrayList<>(adjMatrix.get(vertex));
        /* For cloneMatrix remove vertex and its neighbors */
        cloneMatrix.remove(vertex);
        for (Integer i : neighborhood) cloneMatrix.remove(i);
        for (Integer i : cloneMatrix.keySet()) {
            cloneMatrix.get(i).remove(vertex);
            for (Integer j : neighborhood) cloneMatrix.get(i).remove(j);
        }
        return cloneMatrix;
    }

    private HashMap<Integer, List<Integer>> removeV(HashMap<Integer, List<Integer>> adjMatrix, Integer vertex) {
        HashMap<Integer, List<Integer>> cloneMatrix = copy(adjMatrix);
        /* For adjMatrix remove vertex */
        cloneMatrix.remove(vertex);
        for (Integer i : cloneMatrix.keySet()) {
            cloneMatrix.get(i).remove(vertex); // Integer required instead of int to differ obj from index
        }
        return cloneMatrix;
    }

    private HashMap<Integer, List<Integer>> copy(HashMap<Integer, List<Integer>> adjMatrix) {
        HashMap<Integer, List<Integer>> cloneMatrix = new HashMap<>();
        for (Integer i : adjMatrix.keySet()) {
            ArrayList<Integer> vertices = new ArrayList<>();
            vertices.addAll(adjMatrix.get(i));
            cloneMatrix.put(i, vertices);
        }
        return cloneMatrix;
    }

    private String addDataPath(String file){
        String projectPath = new File("").getAbsolutePath();
        String dataPath = "/independentset/data/";
        return projectPath + dataPath + file;
    }

    private HashMap<Integer, List<Integer>> loadData(String input) {
        HashMap<Integer, List<Integer>> adjMatrix = new HashMap<>();
        try  {
            Scanner s = new Scanner(new File(input));
            /* Read the number of vertices */
            int n = s.nextInt();
            /*
            Initialize the graph as an adjacency matrix with neighbors
            index as list on each vertex, note start index 1 for consistency.*/
            for (int i = 1; i <= n; i++) {
                List<Integer> temp = new ArrayList<>();
                adjMatrix.put(i, temp);
                for (int j = 1; j <= n; j++) {
                    if(s.nextInt() == 1) adjMatrix.get(i).add(j);
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return adjMatrix;
    }
}
