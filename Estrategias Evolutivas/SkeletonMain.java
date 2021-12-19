
import com.codingame.gameengine.runner.SoloGameRunner;

public class SkeletonMain {
    public static void main(String[] args) {
        // Uncomment this section and comment the other one to create a Solo Game
        /* Solo Game */
        SoloGameRunner gameRunner = new SoloGameRunner();
        // Sets the player
        //gameRunner.setAgent(Agent1.class);
        // Sets a test case
        //gameRunner.setTestCase("PyramidScheme.json");
        gameRunner.setTestCase(args[0]);
        // Another way to add a player for python
        //gameRunner.setAgent("python " + String.join(" ", args));
        String pythonArgs = "";
        for(int i = 1; i < args.length; ++i)
            pythonArgs += args[i] + " ";
        gameRunner.setAgent("python " + pythonArgs);
        //gameRunner.setAgent("python BasicAgent.py 92.72703317 122.47712495   0.35140953   1.03682953");

        // Start the game server
        //gameRunner.start();
        // Simulate
        gameRunner.simulate();
        System.out.println("Finished");
    }
}
