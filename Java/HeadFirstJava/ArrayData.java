import java.util.Arrays;

public class ArrayData {
    public static void main (String[] args) {

        //Example of array
        int[] nums;
        nums = new int[3];
        nums[0] = 12;
        nums[1] = 9;
        nums[2] = 6;
        
        //Another way to declare array
        int[] nums1 = {2, 5, 8, 9};
        System.out.println(Arrays.toString(nums));
        System.out.println(Arrays.toString(nums1));
    }
} 
