package com.jobportal;

import static org.junit.Assert.*;
import org.junit.Test;

public class AppTest 
{
    @Test
    public void testAdd() {
        assertEquals(5, App.add(2, 3));
    }

    @Test
    public void testGreet() {
        assertEquals("Hello, Anuj!", App.greet("Anuj"));
    }
}