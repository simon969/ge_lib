

def  calc_M(data)

p1 = (1 - m_KoNC) ^ 2
p2 = (1 + 2 * m_KoNC) ^ 2
p3 = (1 - m_KoNC) * (1 - 2 * m_possonUR) * (m_Lambda / m_Kappa - 1)
p3 = (1 + 2 * m_KoNC) * (1 - 2 * m_poissonUR) * m_Lambda / m_Kappa - (1 - m_KoNC) * (1 + m_poissonUR)

m_M = 3 * (p1 / p2 + p3 / p4) ^ 0.5

End Function
