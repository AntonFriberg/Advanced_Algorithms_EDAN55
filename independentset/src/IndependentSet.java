import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;

/**
 * Created by Anton Friberg on 30/09/16.
 */
public class IndependentSet {

    public static void main(String[] args) {
        IndependentSet s = new IndependentSet();
        s.run();
    }

    private void run() {
        String g4 = addDataPath("g4.in");
        List<List<Integer>> adjMatrix = loadData(g4);
        int result = algR0(adjMatrix);
    }

    private int algR0(List<List<Integer>> adjMatrix) {
        if (adjMatrix.size() == 0) return 0;

        int[] numberOfNeighbors = countNeighbors(adjMatrix);

        /* check for vertex without neighbors */
        for (int i = 0; i < numberOfNeighbors.length; i++) {
            if (numberOfNeighbors[i] == 0) {
                return 1 + algR0(eliminate(i, adjMatrix));
            }
        }

        int maxDegree = 0, vertex = 0;
        

        return 1;
    }

    private List<List<Integer>> eliminate(int pos, List<List<Integer>> adjMatrix) {
        adjMatrix.remove(pos);
        for (List<Integer> list : adjMatrix) {
            list.remove(pos);
        }
        return adjMatrix;
    }

    private int[] countNeighbors(List<List<Integer>> adjMatrix) {
        int[] numberOfNeighbors = new int[adjMatrix.size()];
        int v = 0;
        for (List<Integer> neighbors : adjMatrix) {
            int count = 0;
            for (int i : neighbors) {
                if (i == 1) count++;
            }
            numberOfNeighbors[v++] = count;
        }
        return numberOfNeighbors;
    }

    private static String addDataPath(String file){
        String projectPath = new File("").getAbsolutePath();
        String dataPath = "/independentset/data/";
        return projectPath + dataPath + file;
    }

    private List<List<Integer>> loadData(String input) {
        List<List<Integer>> adjMatrix = new LinkedList<List<Integer>>();
        try (BufferedReader reader = new BufferedReader(new FileReader(input))) {
            String line = reader.readLine();
            /* Read the number of vertices */
            int n = Integer.parseInt(line);
            /* initialize the edges and their weight */
            int i = 0;
            while((line = reader.readLine()) != null) {
                String adjacencyVector[] = line.split(" ");
                int[] tempArray = Arrays.stream(adjacencyVector).mapToInt(Integer::parseInt).toArray();
                List<Integer> tempList= new LinkedList<Integer>();
                for (int j: tempArray) {
                    tempList.add(j);
                }
                adjMatrix.add(tempList);
            }
//            for (int j = 0; j < adjMatrix.size(); j++) {
//                for (int k = 0; k < adjMatrix.get(j).size(); k++) {
//                    System.out.print(" " + adjMatrix.get(j).get(k));
//                }
//                System.out.println();
//            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }
}
