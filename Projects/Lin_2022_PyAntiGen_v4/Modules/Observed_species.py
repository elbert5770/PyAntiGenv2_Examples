def all_species(r):
    observed_species = ['time'] + list(r.getFloatingSpeciesIds()) + list(r.getBoundarySpeciesIds()) + list(r.getAssignmentRuleIds()) + list(r.getGlobalParameterIds())
    return observed_species

def Lin_species(r):
    observed_species = ['time','[AB42_Plasma]', '[Antibody_Plasma]',
    '[AB42__Antibody_Plasma]', '[AB42_Oligomer_Plasma]',
    '[AB42_Oligomer__Antibody_Plasma]','[AB42_BrainISF]',
     '[AB42_Plaque_BrainISF]', '[AB42_Plaque__Antibody_BrainISF]', 
     '[AB42_Plaque__Antibody__FcR_BrainISF]', 
     '[AB42_Oligomer_BrainISF]', '[AB42_Oligomer__Antibody_BrainISF]',
     '[AB42_CSF]', '[AB42_Oligomer_CSF]',
     '[AB42_Oligomer__Antibody_CSF]',
     'totalmAbPlasma', 'totalmAbCSF', 'totalAbetaPlasma', 'totalPlaque', 'totaloligISF',
     'AB42_Plasma', 'Antibody_Plasma',
    'AB42__Antibody_Plasma', 'AB42_Oligomer_Plasma',
    'AB42_Oligomer__Antibody_Plasma',
    'AB42_CSF', 'Antibody_CSF',
    'AB42__Antibody_CSF', 'AB42_Oligomer_CSF',
    'AB42_Oligomer__Antibody_CSF',
    'AB42_BrainISF', 'Antibody_BrainISF',
    'AB42__Antibody_BrainISF', 'AB42_Oligomer_BrainISF',
    'AB42_Oligomer__Antibody_BrainISF',
    'totaloligPlasma', 'totalAbetaBrainISF'
     
     ]
    return observed_species