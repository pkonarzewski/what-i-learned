#%%
import re
from pathlib import Path
import pandas as pd

data_path = Path.cwd()


# %%
rdf = pd.read_csv(data_path / 'contests/other/dane.csv', sep=';')


# %%
df = (
    rdf.melt()
    .loc[lambda x: ~x.value.isnull()]
)
ship_pattern = re.compile(
    r'(?P<ship_id>\d+): '
    r'(?P<ship_name>.+) '
    r'\((?P<ship_class>.+)\)')

ship_info = (df.variable.str.extract(ship_pattern, expand=True)
             .assign(ship_id=lambda x: x.ship_id.apply(int)))

#%%

journey_patter = re.compile(
    r'(?P<container_src>\w+)-'
    r'(?P<container_dest>\w+)-'
    r'(?P<container_no>\d+)/'
    r'(?P<container_weight>\d+)/'
    r'(?P<container_type>\w+)@'
    r'(?P<company_name>.+)\.'
    r'(?P<company_country>.+)/'
    r'(?P<cost>\d+)')
journey_info = (df.value.str.extract(journey_patter, expand=True)
                .assign(container_no=lambda x: x.container_no.apply(int),
                        container_weight=lambda x: x.container_weight.apply(int),
                        cost=lambda x: x.cost.apply(int) / 100.0,
                        company_country=lambda x: x.company_country.str.upper()
                        )
                )


# %%
data_df = ship_info.join(journey_info)
print(data_df.shape)
data_df.tail()


# %% q1
data_df.loc[lambda x: x.container_dest == 'JP',].ship_id.count()


# %% q2
data_df.groupby(['ship_class', 'ship_id']).ship_name.count().reset_index().groupby('ship_class').ship_name.mean().sort_values(ascending=False).head(1)


# %% q3
pd.np.floor(data_df.loc[lambda x: x.container_type == 'X1', 'container_weight'].mean())


# %% q4
# variant 1 - pl comp
data_df.loc[lambda x: x.company_country == 'PL'].groupby('company_name').ship_id.count().sort_values(ascending=False).head(1)

# %% q5
q5 = (data_df.loc[lambda x: (x.company_country == 'DE') & (x.container_src == 'DE')]
 .assign(weight_price=lambda x:  x.cost / x.container_weight)
)

#variant 1
print(q5.sort_values('weight_price', ascending=False).loc[:,['container_type', 'container_weight', 'cost', 'weight_price']].iloc[1,])

# variant 2
q5.groupby('container_type').weight_price.mean().sort_values(ascending=False).head(3)
