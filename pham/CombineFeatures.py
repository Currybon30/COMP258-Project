import pandas as pd

mean_cols = ['High School Average Mark', 'Math Score']
mode_cols = ['Prev Education', 'Age Group', 'English Grade']
fill_with_0_cols = ['1st Term GPA', '2nd Term GPA']
fill_with_3_cols = ['First Language']
passthrough_cols = ['Funding', 'Fast Track', 'Coop', 'Residency', 'Gender']
    
def combine_features(X):
    column_names = mean_cols + fill_with_0_cols + fill_with_3_cols + mode_cols + passthrough_cols
    df_handle_missing = pd.DataFrame(X, columns=column_names)
        
    # Convert the columns to the appropriate types
    num_cols = ['High School Average Mark', 'Math Score', '1st Term GPA', '2nd Term GPA']
    cat_cols = ['First Language', 'Funding', 'Fast Track', 'Coop', 'Residency', 'Gender', 'Prev Education', 'Age Group', 'English Grade']
        
    df_handle_missing[num_cols] = df_handle_missing[num_cols].apply(pd.to_numeric, errors='coerce')
    df_handle_missing[cat_cols] = df_handle_missing[cat_cols].astype('int')
    df_handle_missing[cat_cols] = df_handle_missing[cat_cols].astype('object')
        
    return df_handle_missing