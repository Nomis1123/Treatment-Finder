import pandas as pd

from finder.ai_funcs import GeminiClient as ac
from finder.analysis import SpecialtyAnalyzer as sa
from finder.hospital_finder import HospitalFinder as hf



def main():
    
    
    try:
        ai_client = ac()
        analyzer = sa(ai_client)
        hospital_finder = hf("./Data/hospitalData.csv")
    



if __name__ == "__main__":
    main()
    
    