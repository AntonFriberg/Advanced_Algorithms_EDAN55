import java.io.*;
import java.nio.Buffer;
import java.nio.file.Files;
import java.util.Random;

/**
 * Created by Anton Friberg on 9/25/16.
 * Implementation of the Maximum cut problem.
 */
public class Maxcut {

    private Random r = new Random();
    private int[][] edges;
    private boolean[] choosenVertices;
    private int vertexSize;
    private int numberOfRows;

    public static void main(String[] args) {
        String i1 = addDataPath("pw09_100.9.txt");
        String i2 = addDataPath("matching_1000.txt");
        Maxcut m = new Maxcut();
        m.loadData(i1);
        int iterations = 100000, maxSum = 0;
        for (int i = 0; i < iterations; i++) {
            int temp = m.algR();
            if (temp>maxSum) maxSum = temp;
        }
        System.out.println(maxSum);
    }

    private int algR() {
        /* coin flip to determine if vertex included in set or not */
        choosenVertices = new boolean[vertexSize+1];
        for (int i = 1; i <= vertexSize; i++) {
            choosenVertices[i] = r.nextBoolean();
        }

        int weightSum = 0;
        for (int i[]: edges) {
            int v1     = i[0];
            int v2     = i[1];
            int weight = i[2];

            if (choosenVertices[v1] && choosenVertices[v2]) {
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
            numberOfRows = i;
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
