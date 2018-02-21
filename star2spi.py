from pyem import star
import re
import numpy as np

star_file = 'my_star.star'

df = star.parse_star(star_file)

columns = df.columns
new_columns = []

# Change column names to general column names (without numbers)
for column in columns:
    no_number = column.split()[0]
    new_column_name = re.sub('_rln','',no_number)
    new_columns.append(new_column_name)

df.columns = new_columns

subset_df = df[['GroupNumber','DefocusV','DefocusU','DefocusAngle','AnglePsi','AngleRot','AngleTilt','OriginX','OriginY']]

# Divide OriginX and OriginY by 2
subset_df['OriginX'] = subset_df['OriginX']/2
subset_df['OriginY'] = subset_df['OriginY']/2

# Index by 1 instead of 0
subset_df.index = np.arange(1, len(subset_df) + 1)

# Add a column that just says 9
nine_list = [9]* len(subset_df)
subset_df.insert(0,'9',nine_list)

# And now save our info.spi file!
subset_df.to_csv('info.spi',sep=' ',header=False)





