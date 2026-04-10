README – Debugging Archive for CS3361 Final Project

---------------------------------------------------------------------------------------------------
Purpose

This archive is provided to help you verify and debug your implementation of the CS3361 Final Project. It contains a complete reference run of the simulation on a 10×10 matrix, showing the matrix state at each time step from 0 through 100.


---------------------------------------------------------------------------------------------------
Contents

The archive includes the following files:
	time_step_0.dat
	time_step_1.dat
	time_step_2.dat
	...
	time_step_100.dat


Each file represents the matrix state at the corresponding time step of the simulation.
  -	time_step_0.dat – The input matrix (initial state).

  -	time_step_1.dat through time_step_99.dat – Intermediate states for debugging and logic verification.
	
  -	time_step_100.dat – The final matrix your program should produce after 100 iterations.


---------------------------------------------------------------------------------------------------
Purpose

These files are provided to help you verify the correctness of your implementation.

You can use them to compare your program’s output against a known correct solution at every step of the simulation.


---------------------------------------------------------------------------------------------------
How to Use These Files

Use these reference files to:

  -	Verify that your implementation produces the same results at each time step.

  -	Compare your intermediate outputs to ensure your cell state transitions and wrap-around neighbor logic are functioning correctly.

  -	Confirm that your simulation produces an identical time_step_100.dat result.

These files are provided strictly for debugging and verification. They are not used for grading.


A typical workflow might look like this:

	1. Start with time_step_0.dat as your input.
	2. Run your program for a single iteration.
	3. Compare your result to time_step_1.dat.
	4. Continue this process step-by-step:
		* Your step 2 output → compare with time_step_2.dat
		* Your step 3 output → compare with time_step_3.dat
		* etc.

If your output ever differs from the provided file, you know that the issue occurred in the iteration that produced that step. This makes it much easier to isolate and debug problems.


---------------------------------------------------------------------------------------------------
Final Tip

If your final output (time_step_100.dat) does not match, do not try to debug from the end.

Instead, work forward step-by-step and find the first iteration where your output diverges. That is where the problem begins.


---------------------------------------------------------------------------------------------------
Important for Grading

When graded, your program will be run with its own input file and must only produce a single output file as specified by the -o command-line argument.
That output file must contain only the matrix after the 100th time step.

Your submitted program should not create any additional intermediate output files during grading.
(You may temporarily generate such files for your own debugging, but remove or disable that code before final submission.)