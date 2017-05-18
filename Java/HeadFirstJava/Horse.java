class Horse {
    private double height = 15.2;
    private String breed;
    private int a;
    private int b = 12;

    public int add() {
        int c;
        int total = a + b + c;
        return total;
    }
}

class HorseTestDrive {
    public static void main(String[] args) {
        Horse jim = new Horse();
        int total = jim.add();
        System.out.println(total);
    }
}
