
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings; warnings.filterwarnings(action='once')


if __name__ == '__main__':

    sheet_name="נתוני סקר תיירות נכנסת 2019"
    filepath = r"C:\Users\Anon\Downloads\Dataset-30-11-21.csv"
    #Read file and select columns
    df = pd.read_csv(filepath,encoding= 'unicode_escape',
                     usecols=["How many days prior to your tour did you purchase your flight?", "Country name","TOT_EXP $$"])
    df.columns =["country","total_cost","prior_days"]

    pivot_df = pd.pivot_table(data=df,index=['country'],values=["total_cost","prior_days"],aggfunc=[np.mean])
    pivot_df.columns=["prior_days","total_cost"]

    pivot_df=pivot_df.sort_values("prior_days",ascending=False)
    # select top 5 countries with largest prior_days
    df_top_totalcost_countries=pivot_df.nlargest(5, 'prior_days').index.tolist()
    # filter the countries in original df
    df_top_totalcost=df[df.country.isin(df_top_totalcost_countries)]
    # convert prior_days to 4 bins category
    bins_priorDays = pd.qcut(df_top_totalcost['prior_days'], q=4)
    df_top_totalcost['prior_days']=bins_priorDays

    #create boxplot
    sns.boxplot(orient='h',data=df_top_totalcost,x='total_cost', y='country',hue='prior_days', linewidth=1, showfliers=False)

    plt.show()
