# %%
import pandasql as psql
import pandas as pd


# %%
combine = pd.read_csv(r"\combinefinal.csv")
draft = pd.read_csv(r"\draftfinal.csv")
probowl = pd.read_csv(r"\finalProBowlData.csv")


# %%
draftAndCombine = psql.sqldf("""
    SELECT 
        a.playerId,
        a.combineId,
        a.combineYear,
        a.combinePosition,
        a.combineHeight,
        a.combineWeight,
        a.combineHand,
        a.nameFull,
        a.position,
        a.collegeId,
        a.nflId,
        a.college,
        a.heightInches,
        a.weight,
        a.dob,
        a.ageAtDraft,
        a.playerProfileUrl,
        a.homeCity,
        a.homeState,
        a.homeCountry,
        a.highSchool,
        a.hsCity,
        a.hsState,
        a.hsCountry,
        a.combineArm,
        a.combine40yd,
        a.combineVert,
        a.combineBench,
        a.combineShuttle,
        a.combineBroad,
        a.combine3cone,
        a.combine60ydShuttle,
        a.combineWonderlic,
        b.draft,
        b.round,
        b.pick,
        b.draftTradeValue,
        b.draftTeam,
        b.teamId
    FROM combine AS a
    INNER JOIN draft AS b
    ON a.playerId = b.playerId
""", )


# %%
draftAndCombine.to_csv(r"\draftAndCombine.csv", index=False)


