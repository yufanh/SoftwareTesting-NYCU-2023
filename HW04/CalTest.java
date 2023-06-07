import org.junit.Assert;
import org.junit.Test;


public class CalTest {
    @Test
    public void test1() {
        Assert.assertEquals(0, Cal.cal(2, 29, 2, 29, 2020));
    }

    @Test
    public void test2() {
        Assert.assertEquals(91, Cal.cal(1, 1, 4, 1, 2000));
    }

    @Test
    public void test3() {
        Assert.assertEquals(60, Cal.cal(2, 1, 4, 2, 1800));
    }

    @Test
    public void test4() {
        Assert.assertEquals(92, Cal.cal(3, 5, 6, 5, 2400));
    }

    @Test
    public void test5() {
        Assert.assertEquals(364, Cal.cal(1, 1, 12, 31, 1));
    }

    @Test
    public void test6() {
        Assert.assertEquals(365, Cal.cal(1, 1, 12, 31, 4));
    }

    @Test
    public void test7() {
        Assert.assertEquals(1, Cal.cal(2, 28, 2, 29, 2024));
    }

    @Test
    public void test8() {
        Assert.assertEquals(29, Cal.cal(9, 1, 9, 30, 789));
    }

}
