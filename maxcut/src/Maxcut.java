import java.io.*;
import java.util.Random;

/**
 * Created by Anton Friberg on 9/25/16.
 * Implementation of the Maximum cut problem.
 */
public class Maxcut {

    private Random r = new Random();
    private int[][] edges;
    private boolean[] chosenVertices;
    private int vertexSize;

    public static void main(String[] args) {
        String i1 = addDataPath("pw09_100.9.txt");
        String i2 = addDataPath("matching_1000.txt");
        Maxcut m = new Maxcut();
        m.loadData(i1); //initialize graph from given data
        int iterations = 100, maxSum = 0; // number of random sets to run
        for (int i = 0; i < iterations; i++) {
            int temp = m.algR();
            if (temp>maxSum) maxSum = temp;
        }
        System.out.println(maxSum);
    }

    private int algR() {
        int weightSum = 0;
        /* coin flip to determine if vertex included in set or not */
        chosenVertices = new boolean[vertexSize+1];
        for (int i = 1; i <= vertexSize; i++) {
            chosenVertices[i] = r.nextBoolean();
        }
        /* add weight to sum if both vertices chosen by coin flip */
        for (int i[]: edges) {
            int v1     = i[0];
            int v2     = i[1];
            int weight = i[2];
            if (chosenVertices[v1] && chosenVertices[v2]) {
                weightSum += weight;
            }
        }
        return weightSum;
    }

    private static String addDataPath(String file){
        String projectPath = new File("").getAbsolutePath();
        String dataPath = "/maxcut/data/";
        return projectPath + dataPath + file;
    }

    private void loadData(String input) {
        vertexSize = 0;
        try (BufferedReader reader = new BufferedReader(new FileReader(input))) {
            String line = reader.readLine();

            /* Read the number of vertices and edges on the first line */
            String graphProperties[] = line.split(" ");
            vertexSize = Integer.parseInt(graphProperties[0]);
            int edgeSize = Integer.parseInt(graphProperties[1]);
            edges = new int[edgeSize][];

            /* initialize the edges and their weight */
            int i = 0;
            while((line = reader.readLine()) != null) {
                String vertexProperties[] = line.split(" ");
                int v1     = Integer.parseInt(vertexProperties[0]);
                int v2     = Integer.parseInt(vertexProperties[1]);
                int weight = Integer.parseInt(vertexProperties[2]);
                edges[i++] = new int[]{v1,v2,weight};
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
