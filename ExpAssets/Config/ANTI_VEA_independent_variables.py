from klibs.KLIndependentVariable import IndependentVariableSet


# Initialize object containing project's independent variables

ANTI_VEA_ind_vars = IndependentVariableSet()


# Define project variables and variable types

## Factors ##
# 'trial_type': the type of trial (ANTI, EV, or AV)
#   - 'ANTI': ANTI trials that can be validly cued, invalidly cued, or uncued
#   - 'EV': Executive vigilance trials where the central arrow displacement can be
#           either above or below the surrounding flankers
#   - 'AV': Arousal vigilance (PVT) trials
# 'cue_type': the type of cue ("valid" == same location as 'target_location')
# 'target_location': the location of the target and flanker arrows
# 'congruent': whether the direction of the flanker arrows matches the target arrows

trial_types = [
    ('ANTI-valid', 2), ('ANTI-invalid', 2), ('ANTI-none', 2),
    'EV-above', 'EV-below',
    ('AV', 2)
]

ANTI_VEA_ind_vars.add_variable('trial_type', str, trial_types)
ANTI_VEA_ind_vars.add_variable('tone_trial', bool, [True, False])
ANTI_VEA_ind_vars.add_variable('target_location', str, ['above', 'below'])
ANTI_VEA_ind_vars.add_variable('congruent', bool, [True, False])
