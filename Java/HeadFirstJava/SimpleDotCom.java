//import java.util.Integer;

class SimpleDotCom {
    private int[] locationCells;
    private int numberOfHits;

    public String checkYourself(String userGuess) {
        int guess = Integer.parseInt(userGuess);
        String result = "miss";

        for (int cell : locationCells) {
            if ( guess == cell ) {
                result = "hit";
                numberOfHits++;
                break;
            }
        }

        if (numberOfHits == locationCells.length) {
            result = "kill";
        } 

        System.out.println(result);
        return result;
    }

    public void setLocationCells(int[] locCells) {

        locationCells = locCells;
        
    }
}

class SimpleDotComTestDrive {
    public static void main(String[] args) {
        int[] locations = {2, 4, 6};
        SimpleDotCom dot = new SimpleDotCom();
        dot.setLocationCells(locations);
        
        String userGuess = "2";
        String result = dot.checkYourself(userGuess);
    }
}

class SimpleDotComGame {
    public static void main(String[] args) {
        
    }
}
