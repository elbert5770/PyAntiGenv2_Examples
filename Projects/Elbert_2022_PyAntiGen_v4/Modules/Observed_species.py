def all_species(r):
    observed_species = ['time'] + list(r.getFloatingSpeciesIds()) + list(r.getBoundarySpeciesIds()) + list(r.getAssignmentRuleIds()) + list(r.getGlobalParameterIds())
    return observed_species

def SILK_species(r):
    observed_species = ['time','f_13C6Leu','[APP_BrainISF]','[AB40_BrainISF]','[AB42_BrainISF]',
    '[C99_BrainISF]','[AB40_SAS]','[AB40_CV]','[AB40_SP3]','[AB42_SAS]','[AB42_CV]','[AB42_SP3]',
    '[AB38_BrainISF]','[AB38_SAS]','[AB38_CV]','[AB38_SP3]','[AB38_13C6Leu_SP3]','[AB40_13C6Leu_SP3]','[AB42_13C6Leu_SP3]',
    'Q_LP','f_13C6Leu','[AB38_13C6Leu_BrainISF]','[AB40_13C6Leu_BrainISF]','[AB42_13C6Leu_BrainISF]',
    'Q_SN','Q_refill','Q_Leak', 'V_SP3','AB40_SP3','AB40_13C6Leu_SP3','[AB40_13C6Leu_CV]','[AB40_13C6Leu_SAS]','[AB40_13C6Leu_SP1]','[AB40_13C6Leu_SP2]','[AB40_13C6Leu_SP3]',
    '[AB40_SP1]','[AB40_SP2]','[AB42_SP1]','[AB42_SP2]','[AB38_SP1]','[AB38_SP2]','AB40_SP2','AB40_13C6Leu_SP2',
    'V_SP2','SF38','SF40','SF42']
    return observed_species