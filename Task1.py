# -*- coding: utf-8 -*-

"""
Task 1 of QOSF mentorship program
"""

from matplotlib.pyplot import flag
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute

from math import pi

def multiplication(A , B):

    def decimal_to_binary(n):
        return bin(n).replace("0b", "")

    def binary_to_decimal(n):
        return int(n,2)

    def QFT(cir, q_reg, n):
        qc.h(q_reg[n])
        for k in range (0,n):
            cir.cp(pi/float(2**(k+1)), q_reg[n - (k+1)], q_reg[n])

    def IQFT(cir,q_reg, n):
        for k in range(0, n):
            cir.cp(-1 * pi / float(2**(n - k)), q_reg[k], q_reg[n])
        cir.h(q_reg[n])

    def QFT_adder(cir, reg_x, reg_y, n, factor):
        l = len(reg_y)
        for k in range (0, n+1):
            if (n - k ) > l - 1:
                pass
            else:
                cir.cp(factor*pi /  float(2**(k)),reg_y[n - k], reg_x[n])

    def sum(reg_x, reg_y, qc, factor):
        n = len(reg_x) - 1
    
        for k in range(0, n+1):
            QFT(qc, reg_x, n-k)
    
        for k in range(0, n+1):
            QFT_adder(qc, reg_x, reg_y, n-k, factor)
    
        for k in range(0, n+1):
            IQFT(qc, reg_x, k)

    # input -> decimal to binary 
    multiplicand = decimal_to_binary(A)
    multiplier = decimal_to_binary(B)

    # having larger string as multiplicant 
    if (len(multiplier) > len(multiplicand)):
        multiplier, multiplicand = multiplicand, multiplier

    c_reg = ClassicalRegister(len(multiplicand)+ len(multiplier))

    adder = QuantumRegister(len(multiplicand)+ len(multiplier))
    decrease = QuantumRegister(1)
    multiplicand_reg = QuantumRegister(len(multiplicand))
    multiplier_reg = QuantumRegister(len(multiplier))

    qc = QuantumCircuit(adder, multiplier_reg, multiplicand_reg, decrease, c_reg, name = "cir")

    #decrease state -> |1>
    qc.x(decrease)

    #storing value in register
    for i in range(len(multiplicand)):
        if (multiplicand[i] == '1'):
            qc.x(multiplicand_reg[len(multiplicand)-i-1])
    
    for i in range(len(multiplier)):
        if (multiplier[i] == '1'):
            qc.x(multiplier_reg[len(multiplier)-i-1])

    Flag = 1

    while(int(Flag)):
        sum(adder, multiplicand_reg, qc, 1)
    
        sum(multiplier_reg, decrease, qc, -1)
    
        for j in range(len(multiplier_reg)):
            qc.measure(multiplier_reg[j], c_reg[j])
        job = execute(qc, backend = Aer.get_backend('qasm_simulator'), shots = 2)
        counts = job.result().get_counts(qc)
        Flag  = binary_to_decimal(list(counts.keys())[0])

    qc.measure(adder, c_reg)

    job = execute(qc, backend = Aer.get_backend('qasm_simulator'), shots = 2)
    counts = job.result().get_counts(qc)

    product = binary_to_decimal(next(iter(counts)))   
    return(product)
