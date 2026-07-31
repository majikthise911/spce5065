# SPCE 5065 HOMEWORK #3

## DUE: Friday 3 July 2026

All homework is due in Canvas by 11:59:59 pm MT (Colorado Time) on the due date indicated on the Syllabus schedule. No late homework will be accepted.

Students are allowed PARTIAL COLLABORATION on homework assignments. You are allowed to discuss qualitatively with other students the concepts in this course. However, copying or in way using the written work of another person as well as relaying or receiving solutions via any means is strictly prohibited. The intent of this policy is to allow you to share ideas, discuss concepts, and clarify processes when needed. However, you must independently prepare the detailed solutions to homework problems and the Final Project.

Use course readings as a resource, but research additional sources as necessary to answer the questions. Please annotate your research with [1] , [2], etc. and a sources page that describe where the information is located in AIAA format. Please email me with any questions or concerns.

Clearly state any assumptions you make.

- 1. A 100 kg satellite with an effective cross-sectional area of 1 m2is in a circular earth orbit at an altitude of 400 km. Its drag coefficient is 2.2. A rough estimate of the atmospheric density in the thermosphere is given by:


![image 1](img/Homework_2_Solution_0.png)

Estimate the satellite’s lifetime if you assume the spacecraft deorbits at an altitude of 150 km. Do not assume an average R value as we did for the in-class exercise.

Solution: Using material from lesson 5 in-class exercise:

𝑑𝑎 𝑑𝑡

𝐶𝐷𝐴 𝑚

√𝜇𝑎 See attached Matlab Code

= −𝜌

Lifetime estimate = 221.5 days

- 2. How much drag makeup fuel is needed for the spacecraft in problem 1 to maintain its original orbit for one year? Assume average solar cycle conditions and monopropellant fuel with an Isp = 200 seconds. Use your model from part 1 to find the atmospheric density.


FDRAG = 0.5*ρ*CD*A*V2 ρ = 2.2432 * 10-12 kg/m3

- FDRAG = 0.5*2.2432 * 10-12 kg/m3* 2.2 * 1m2* 398600.5

𝑘𝑚3 𝑠2

6778 𝑘𝑚 *(1000 𝑚)

2 𝑘𝑚2

- FDRAG = 1.45 x 10-4 N


−4 𝑁∗365∗24∗3600 𝑠𝑒𝑐𝑜𝑛𝑑𝑠 200 𝑠𝑒𝑐𝑜𝑛𝑑𝑠∗9.81 𝑠𝑚2

𝑚′ = 𝐹∆𝑡𝑣′ = 𝐼𝐹∆𝑡

𝑠𝑝𝑔𝑜 = 1.45 𝑥 10

|𝑚′ = 2.33 𝑘𝑔|
|---|


#### 3. Determine the erosion depth per year of a Kapton panel of a spacecraft oriented in the RAMdirection (the side that points in the direction of the satellite’s velocity vector) at an altitude of450 km during low, medium, and high solar activity. The atomic-oxygen number densities are 6x 106, 2 x 107, and 1 x 108 atoms/cm3, respectively.

![image 2](img/Homework_2_Solution_1.png)

#### 4. The Apollo command module has a volume of 5.9 m3 and its atmosphere is 100% oxygen at apressure of 5 psia and temperature of 21°C.

- a. Determine the mass of oxygen present.
- b. Would you recommend this atmosphere for a human vehicle bound for Mars? If not, what would you recommend?


![image 3](img/Homework_2_Solution_2.png)

No. Pure oxygen presents a fire hazard. I would recommend a mixture more like the earth’s atmosphere of approximately 78% Nitrogen and 21% oxygen. We do not know what the long term (> 6 months) effects will be for breathing pure oxygen.

#### 5. Create a plot of the lifetime of the satellite in problem 1 for all starting orbit altitudesbetween 200 and 600 km.

- 6. The International Space Station uses Kapton for some applications.


- a. What is Kapton used for on the ISS?

Answers may vary depending on the reference used. Common uses are for thermal control, atomic oxygen protection, and tape to repair electronic components.

- b. Estimate the erosion of Kapton on the ISS for a mission of one year that is due to atomic oxygen.


![image 4](img/Homework_2_Solution_3.png)
