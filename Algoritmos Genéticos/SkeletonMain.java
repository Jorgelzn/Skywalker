
import com.codingame.gameengine.runner.SoloGameRunner;

public class SkeletonMain {
    public static void main(String[] args) {
        // Uncomment this section and comment the other one to create a Solo Game
        /* Solo Game */
        SoloGameRunner gameRunner = new SoloGameRunner();
        // Sets the player
        //gameRunner.setAgent(Agent1.class);
        // Sets a test case
        gameRunner.setTestCase(args[0]);

        // Another way to add a player for python
        gameRunner.setAgent("python agente_gen.py");

        // Start the game server
        //gameRunner.start();
        // Simulate
        gameRunner.simulate();
    }
}
