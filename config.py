NUM_COLS = [
    'Age','DailyRate','DistanceFromHome','Education','EnvironmentSatisfaction',
    'JobInvolvement','JobLevel','JobSatisfaction','MonthlyIncome','MonthlyRate',
    'NumCompaniesWorked','PerformanceRating','RelationshipSatisfaction',
    'StockOptionLevel','TotalWorkingYears','TrainingTimesLastYear',
    'WorkLifeBalance','YearsAtCompany','YearsInCurrentRole',
    'YearsSinceLastPromotion','YearsWithCurrManager'
]

CAT_COLS = [
    'BusinessTravel','Department','EducationField','Gender',
    'JobRole','MaritalStatus','OverTime'
]

ENG_COLS = [
    'SatisfactionScore','IncomePerYear','PromotionGap',
    'IsOvertime','LowSatOvertime','StuckInRole'
]

ALL_FEATURES = NUM_COLS + CAT_COLS + ENG_COLS