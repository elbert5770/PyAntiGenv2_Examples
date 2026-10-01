def all_species(r):
    observed_species = ['time'] + list(r.getFloatingSpeciesIds()) + list(r.getBoundarySpeciesIds()) + list(r.getAssignmentRuleIds()) + list(r.getGlobalParameterIds())
    return observed_species

def Bloomingdale_species(r):
    observed_species = ['time', '[Antibody_BBB]','[Antibody_BCSFB]','[Antibody_BrainISF]','[Antibody_BrainVascular]','[Antibody_CSF]',
    '[Antibody_Lymph]','[Antibody_Plasma]','[Antibody_TissueEndosomal]','[Antibody_TissueISF]','[Antibody_TissueVascular]',
    '[Antibody__FcRn_BBB]','[Antibody__FcRn_BCSFB]','[Antibody__FcRn_TissueEndosomal]','[FcRn_BBB]','[FcRn_BCSFB]','[FcRn_TissueEndosomal]',
    '[Gadobutrol_Plasma]','[Gadobutrol_CSF]','[Gadobutrol_BBB]','[Gadobutrol_BCSFB]','[Gadobutrol_BrainISF]','[Gadobutrol_BrainVascular]',
    '[Gadobutrol_Lymph]','[Gadobutrol_TissueEndosomal]','[Gadobutrol_TissueISF]','[Gadobutrol_TissueVascular]']
    return observed_species