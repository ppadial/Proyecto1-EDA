def convertir_tipos(df):
    # --- Conversiones a categóricas ---
    df['type']   = df['type'].astype('category')
    df['status'] = df['status'].astype('category')
    #df['studios'] = df['studios'].astype('category')
    df['source'] = df['source'].astype('category')

    # rating como categórica ORDENADA
    orden_rating = ['G', 'PG', 'PG-13', 'R', 'R+', 'Rx']
    df['rating'] = pd.Categorical(df['rating'], categories=orden_rating, ordered=True)

    # --- Conversiones a enteros "nullable" (Int64) ---
    df['episodes']    = df['episodes'].astype('Int64')
    df['aired_start'] = df['aired_start'].astype('Int64')
    df['rank']        = df['rank'].astype('Int64')
    df['scored_by']   = df['scored_by'].astype('Int64')
    return df