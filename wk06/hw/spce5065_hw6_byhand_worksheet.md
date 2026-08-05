# SPCE 5065 - HW6 By-Hand Calculation Worksheet

Six sheets. **Q2, Q6, and Q8 are worth doing entirely by hand** (clean closed-form
chains). **Q4 and Q5 get one worked case each** and the script carries the other
eight bodies. **Q7 is a single evaluation** and the plot carries the rest.

Every step carries units. Work the blank column, then check the answer key at the
bottom. Q3 is not here on purpose: it needs numerical integration of Planck's law.

**Constants (all from the assignment sheet or Lesson 6):**

| Symbol | Value | Units |
|---|---|---|
| $h$ | $6.626\times10^{-34}$ | J s |
| $c$ | $2.998\times10^{8}$ | m/s |
| $hc$ | $1.986\times10^{-25}$ (= $1.24$ eV $\mu$m) | J m |
| 1 eV | $1.602\times10^{-19}$ | J |
| $k$ (Boltzmann) | $1.381\times10^{-23}$ | J/K |
| $\sigma$ (Stefan-Boltzmann) | $5.67\times10^{-8}$ | W m$^{-2}$ K$^{-4}$ |
| $b$ (Wien) | $2.898\times10^{-3}$ | m K |
| $T_{sun}$ | $5772$ | K |
| $L_{sun}$ | $3.828\times10^{26}$ | W |
| 1 AU | $1.496\times10^{11}$ | m |
| $S_\oplus$ (solar constant) | $1367$ | W/m$^2$ |
| $R_E$ | $6378$ | km |
| $R$ (gas constant) | $62.364$ | L Torr mol$^{-1}$ K$^{-1}$ |
| 1 Torr | $133.322$ | Pa |
| 1 mil | $0.00254$ | cm |

---

## Sheet 1 - Q2: bond-breaking photon flux (parts a, c, d)

### (a) Cutoff wavelength

$$E = \frac{hc}{\lambda} \;\;\Longrightarrow\;\; \lambda_{max} = \frac{hc}{E_{bond}}$$

**Given:** $E_{bond} = 3.47$ eV for a single C-C bond.

| Step | Work |
|---|---|
| 1. eV to joules | ____________________________________________ |
| 2. Divide $hc$ by it | ____________________________________________ |
| 3. Convert m to $\mu$m | ____________________________________________ |

**Answer:** $\lambda_{max} =$ ______________ $\mu$m

> **Shortcut worth knowing:** $hc = 1.24$ eV $\mu$m, so this is one division. Use it to check step 2.

### (c) Photons in the band

Dividing irradiance by $hc/\lambda$ pulls a $\lambda$ into the numerator:

$$N = \frac{1}{hc}\int_{\lambda_0}^{\lambda_{max}} S(\lambda)\,\lambda\,d\lambda$$

**Given** (take the fit from the script, do not try to least-squares five points by hand):

$$S(\lambda) = 0.6585\,\lambda - 0.1373 \quad [\text{W cm}^{-2}\ \mu\text{m}^{-1}],\qquad \lambda_0 = 0.2085\ \mu\text{m}$$

| Step | Work |
|---|---|
| 1. Expand the integrand $(m\lambda + b)\lambda$ | ____________________________________________ |
| 2. Antiderivative $\frac{m\lambda^3}{3} + \frac{b\lambda^2}{2}$ | ____________________________________________ |
| 3. Evaluate at $\lambda_{max} = 0.3573$ | ____________________________________________ |
| 4. Evaluate at $\lambda_0 = 0.2085$ | ____________________________________________ |
| 5. Subtract | ____________________________________________ |
| 6. $\times 10^{-6}$ ($\mu$m to m for $hc$) | ____________________________________________ |
| 7. Divide by $hc$ | ____________________________________________ |

**Answer:** $N =$ ______________ photons cm$^{-2}$ s$^{-1}$

> **The trap is step 6.** The integral carries $\mu$m because $\lambda$ was in microns, but $hc$ is in J m. Skip it and the answer is off by exactly $10^{6}$.

### (d) Total photon output and the fraction

| Step | Work |
|---|---|
| 1. Wien: $\lambda_{peak} = b/T_{sun}$ | ____________________________________________ |
| 2. $E_{avg} = hc/\lambda_{peak}$ (J, then eV) | ____________________________________________ |
| 3. $\dot N_{sun} = L_{sun}/E_{avg}$ | ____________________________________________ |
| 4. $4\pi r^2$ at 1 AU | ____________________________________________ |
| 5. Divide, then convert to cm$^{-2}$ | ____________________________________________ |
| 6. Fraction: (c) divided by (5) | ____________________________________________ |

**Answers:** $N_{total} =$ ______________ cm$^{-2}$ s$^{-1}$ &nbsp;&nbsp; fraction $=$ _________ %

> **Free check on step 5:** $S_\oplus/E_{avg} = 1367/E_{avg}$ should reproduce the same flux, because it is the same calculation with $4\pi r^2$ already applied.

---

## Sheet 2 - Q4: probe equilibrium temperature (Earth case only)

$$Q_{solar} + Q_{albedo} + Q_{IR} + Q_{int} = \epsilon\sigma A_{tot} T^4$$
$$Q_{solar} = \alpha A S, \quad Q_{albedo} = \alpha A \sin^2\!\rho\,(a_{geo}S), \quad Q_{IR} = \alpha A \sin^2\!\rho\,F_{IR}, \quad \sin\rho = \frac{R_p}{R_p+h}$$

**Given:** $\alpha = 0.3$, $\epsilon = 0.7$, 1 m cube so $A = 1$ m$^2$ in and $A_{tot} = 6$ m$^2$ out,
$Q_{int} = 750$ W, $h = 1000$ km, $R_E = 6378$ km, $S = 1367$ W/m$^2$, Earth albedo $a_{geo} = 0.37$,
Earth $F_{IR} = 237$ W/m$^2$. Use $\alpha$ on the IR term, per the Lesson 6 slide-30 form.

| Step | Work |
|---|---|
| 1. $\sin\rho = 6378/(6378+1000)$ | ____________________________________________ |
| 2. $\rho$ in degrees | ____________________________________________ |
| 3. $\sin^2\rho$ | ____________________________________________ |
| 4. $Q_{solar}$ | ____________________________________________ |
| 5. Albedo flux $= a_{geo}S$ | ____________________________________________ |
| 6. $Q_{albedo}$ | ____________________________________________ |
| 7. $Q_{IR}$ | ____________________________________________ |
| 8. $Q_{total}$ (add $Q_{int}$) | ____________________________________________ |
| 9. Denominator $\epsilon\sigma A_{tot}$ | ____________________________________________ |
| 10. $T^4 = Q_{total}/(\epsilon\sigma A_{tot})$ | ____________________________________________ |
| 11. $T$ (fourth root), then $^\circ$C | ____________________________________________ |

**Answer:** $T_{sun} =$ ______________ K $=$ ______________ $^\circ$C

> **Eclipse case, same sheet:** drop $Q_{solar}$ and $Q_{albedo}$, keep $Q_{IR} + Q_{int}$, rerun steps 10 and 11.
> **Common slip:** using 1 m$^2$ on both sides. Heat comes in on one face and leaves on all six; getting that wrong scales $T$ by $6^{1/4} = 1.57$.

---

## Sheet 3 - Q6: Neoprene outgassing (parts a and b)

### (a) The conversion factor

Part (a) asks you to *show* the factor, so the derivation is the answer.

| Step | Work |
|---|---|
| 1. 1 Torr L in joules ($133.322 \times 10^{-3}$) | ____________________________________________ |
| 2. Per cm$^2$ per s, area to m$^2$ ($\div 10^{-4}$) | ____________________________________________ |
| 3. Invert for 1 W/m$^2$ | ____________________________________________ |
| 4. Apply to $10^{-5}$ Torr L cm$^{-2}$ s$^{-1}$ | ____________________________________________ |

**Answers:** 1 W/m$^2$ $=$ ______________ Torr L cm$^{-2}$ s$^{-1}$ &nbsp;&nbsp; $\dot Q =$ ______________ W/m$^2$

### (b) Molecules per unit area per second

$$PV = NkT \;\;\Longrightarrow\;\; \dot N = \frac{\dot Q}{kT}$$

| Step | Work |
|---|---|
| 1. $kT$ at 298 K | ____________________________________________ |
| 2. Divide $\dot Q$ by $kT$ (per m$^2$) | ____________________________________________ |
| 3. Convert to per cm$^2$ | ____________________________________________ |

**Answer:** $\dot N =$ ______________ molecules cm$^{-2}$ s$^{-1}$

> **Why this works at all:** pressure $\times$ volume $=$ N/m$^2$ $\times$ m$^3$ $=$ N m $=$ J. The odd-looking unit was a power per unit area the whole time.

---

## Sheet 4 - Q8: Kapton outgassing rate from a TML

**State the assumptions first** (they are part of the grade): 24 h ASTM E-595 test
duration, rate referenced to 298 K, 10 cm $\times$ 10 cm coupon with only the top
face exposed, all TML leaving as an ideal gas at $M = 15$ g/mol.

**Given:** $A = 100$ cm$^2$, $t = 0.001$ in, $\rho = 1.5$ g/cm$^3$, TML $= 0.5\%$,
$M = 15$ g/mol, duration $= 86{,}400$ s, $T = 298$ K.

| Step | Work |
|---|---|
| 1. Thickness in cm | ____________________________________________ |
| 2. Volume $= A \times t$ | ____________________________________________ |
| 3. Mass $= \rho V$ | ____________________________________________ |
| 4. $\Delta m = 0.005\,m$ | ____________________________________________ |
| 5. Moles $n = \Delta m/M$ | ____________________________________________ |
| 6. $PV = nRT$ (Torr L) | ____________________________________________ |
| 7. Divide by area $\times$ time | ____________________________________________ |
| 8. Convert to W/m$^2$ ($\times 1333.22$) | ____________________________________________ |

**Answers:** $\dot Q =$ ______________ Torr L cm$^{-2}$ s$^{-1}$ $=$ ______________ W/m$^2$

> **Cross-check:** Pisacane Table 10.3 lists Kapton foil near $1\times10^{-4}$ W/m$^2$. Landing within a factor of a few confirms nothing is off by orders of magnitude.
> **Note on the typo:** "10 m x 10 cm" gives the identical answer, since scaling one dimension scales mass and area together and the result is a rate per unit area.

---

## Sheet 5 - Q5: the mass budget and the two bounding cases

### The budget

| Step | Work |
|---|---|
| 1. Mass allowance $= \$15{,}000 / \$25{,}000$ per kg | ____________________________________________ |
| 2. Louvers, 1 m$^2$: $(2.1 + 0.2)$ kg $\times$ cost | ____________________________________________ |
| 3. MLI, 2 m$^2$: $2(0.3)$ kg $\times$ cost | ____________________________________________ |

**Answers:** allowance $=$ _________ kg &nbsp;&nbsp; MLI cost $=$ ______________

### The two bounding temperatures

Design: MLI ($\alpha = \epsilon = 0.05$) on the sun and nadir faces, white paint
($\epsilon = 0.85$) on the other four.

| Step | Work |
|---|---|
| 1. $\sum \epsilon_i A_i = 4(0.85) + 2(0.05)$ | ____________________________________________ |
| 2. Mercury hot: $Q = 1338.3$ W, solve $T$ | ____________________________________________ |
| 3. Pluto cold: $Q = 750.0$ W, solve $T$ | ____________________________________________ |

**Answers:** $T_{Mercury} =$ ______________ $^\circ$C &nbsp;&nbsp; $T_{Pluto} =$ ______________ $^\circ$C

> **The elegant bit, worth writing on the page:** both cases radiate through the same $\sum\epsilon A$, so $T_{hot}/T_{cold} = (Q_{hot}/Q_{cold})^{1/4} = 1.156$ regardless of the emissivity chosen. One knob has to satisfy both limits, and it does for any $\epsilon$ from 0.63 to 1.00.

---

## Sheet 6 - Q7: one ISO evaluation

$$C_n = 10^{N}\left(\frac{0.1\ \mu\text{m}}{D}\right)^{2.08}$$

Work ISO Class 5 at $D = 0.5\ \mu$m and check it against the published table.

| Step | Work |
|---|---|
| 1. Ratio $0.1/0.5$ | ____________________________________________ |
| 2. $\log_{10}$ of the ratio | ____________________________________________ |
| 3. $\times 2.08$ | ____________________________________________ |
| 4. Antilog | ____________________________________________ |
| 5. $\times 10^5$ | ____________________________________________ |

**Answer:** $C_5(0.5\ \mu$m$) =$ ______________ particles/m$^3$

> **Check:** ISO 14644-1 tabulates 3,520 for this cell. Matching to rounding confirms both the exponent and the $0.1\ \mu$m reference size.

---

## Answer key (cover until you have worked them)

| Sheet | Quantity | By-hand answer | Script target |
|---|---|---|---|
| Q2a | $E_{bond}$ in J | $5.560\times10^{-19}$ J | `5.5596e-19 J` |
| Q2a | $\lambda_{max}$ | $0.357\ \mu$m | `0.3573 um` |
| Q2c | Integral (before $10^{-6}$) | $0.002242$ W $\mu$m cm$^{-2}$ | `2.242e-3` |
| Q2c | $N$ in band | $1.13\times10^{16}$ cm$^{-2}$s$^{-1}$ | `1.1293e16` |
| Q2d | $\lambda_{peak}$ | $0.502\ \mu$m | `0.5020 um` |
| Q2d | $E_{avg}$ | $3.957\times10^{-19}$ J $= 2.47$ eV | `2.470 eV` |
| Q2d | $\dot N_{sun}$ | $9.67\times10^{44}$ /s | `9.6745e44` |
| Q2d | $4\pi r^2$ | $2.812\times10^{23}$ m$^2$ | `2.8123e23` |
| Q2d | $N_{total}$ | $3.44\times10^{17}$ cm$^{-2}$s$^{-1}$ | `3.4401e17` |
| Q2d | Fraction | $3.3\%$ | `3.28 %` |
| Q4 | $\sin\rho$ / $\rho$ / $\sin^2\rho$ | $0.8645$ / $59.82^\circ$ / $0.7473$ | `0.7473` |
| Q4 | $Q_{solar}$ / $Q_{albedo}$ / $Q_{IR}$ | $410.1$ / $113.4$ / $53.1$ W | `410.1 / 113.4 / 53.1` |
| Q4 | $Q_{total}$ | $1326.6$ W | `1326.6 W` |
| Q4 | $\epsilon\sigma A_{tot}$ | $2.381\times10^{-7}$ | `2.3814e-7` |
| Q4 | $T$ sunlit | $273.2$ K $= 0.0\ ^\circ$C | `0.0 C` |
| Q4 | $T$ eclipse | $241.0$ K $= -32.2\ ^\circ$C | `-32.2 C` |
| Q6a | 1 Torr L | $0.133322$ J | `0.133322 J` |
| Q6a | Conversion | $1333.22$ W/m$^2$; inverse $7.50\times10^{-4}$ | `7.5006e-4` |
| Q6a | $\dot Q$ | $1.333\times10^{-2}$ W/m$^2$ | `1.3332e-2` |
| Q6b | $kT$ at 298 K | $4.114\times10^{-21}$ J | `4.114e-21` |
| Q6b | $\dot N$ | $3.24\times10^{14}$ cm$^{-2}$s$^{-1}$ | `3.2404e14` |
| Q8 | Volume / mass | $0.2540$ cm$^3$ / $0.3810$ g | `0.2540 / 0.3810` |
| Q8 | $\Delta m$ / moles | $1.905\times10^{-3}$ g / $1.270\times10^{-4}$ mol | `1.2700e-4 mol` |
| Q8 | $PV$ | $2.360$ Torr L | `2.3602` |
| Q8 | $\dot Q$ | $2.73\times10^{-7}$ Torr L cm$^{-2}$s$^{-1}$ | `2.7317e-7` |
| Q8 | $\dot Q$ in SI | $3.64\times10^{-4}$ W/m$^2$ | `3.6420e-4` |
| Q5 | Mass allowance | $0.60$ kg | `0.60 kg` |
| Q5 | Louvers / MLI cost | \$57,500 / \$15,000 | `57,500 / 15,000` |
| Q5 | $\sum\epsilon A$ | $3.50$ m$^2$ | `3.50` |
| Q5 | $T$ Mercury / Pluto | $13.4$ / $-25.2\ ^\circ$C | `13.4 / -25.2` |
| Q7 | $C_5$ at $0.5\ \mu$m | $3517$ /m$^3$ | `3516.8` (table: 3,520) |

**Unit discipline reminders, in the order they will bite you:**

1. **Q2c:** the $10^{-6}$ converting $\mu$m to m before dividing by $hc$.
2. **Q4:** temperature in **kelvin** inside the fourth power, and one face in against six faces out.
3. **Q6 and Q8:** the $10^{-4}$ converting cm$^2$ to m$^2$, and $k$ per molecule against $R$ per mole.
4. **Q8:** thickness in cm before multiplying by an area in cm$^2$, and grams against kilograms in the molar mass step.
