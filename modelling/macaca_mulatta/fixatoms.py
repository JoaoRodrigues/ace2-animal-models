from modeller import *
from modeller.automodel import *
from modeller.parallel import *

# These classes select for refinement the atoms of residues that differ
# between the template and the model

class MyModel_loop(loopmodel):
    def select_atoms(self):
        
        # Read alignment
        aln = self.read_alignment()

        # Get template/model sequences
        template, model = None, None
        for key in aln:
            if key.prottyp.startswith('sequence'):
                model = key
            elif key.prottyp.startswith('structure'):
                template = key

        assert model is not None and template is not None

        # Get positions where the model differs from the template
        mutations = []
        for pos in aln.positions:
            t_res = pos.get_residue(template)
            m_res = pos.get_residue(model)
            
            if m_res is None:  # deletion
                continue

            elif t_res is None:  # insertion
                resi = m_res.index
                resrange = self.residue_range(
                    f'{resi}:A', f'{resi}:A'
                )

                print(f'(loopmodel) Unfreezing {resi}A')
                mutations.append(resrange)

            elif t_res.name != m_res.name:
                resi = m_res.index
                resrange = self.residue_range(
                    f'{resi}:A', f'{resi}:A'
                )

                print(f'(loopmodel) Unfreezing {resi}A')
                mutations.append(resrange)

        if not mutations:
            # Dummy region of the ACE2 protein.
            # MODELLER needs something to optimize

            print('(loopmodel) unfreezing single residue')
            return selection(self.residue_range('580:A', '580:A'))

        return selection(mutations)


class MyModel_auto(automodel):
    def select_atoms(self):
        
        # Read alignment
        aln = self.read_alignment()

        # Get template/model sequences
        template, model = None, None
        for key in aln:
            if key.prottyp.startswith('sequence'):
                model = key
            elif key.prottyp.startswith('structure'):
                template = key

        assert model is not None and template is not None

        # Get positions where the model differs from the template
        mutations = []
        for pos in aln.positions:
            t_res = pos.get_residue(template)
            m_res = pos.get_residue(model)
            
            if m_res is None:  # deletion
                continue

            elif t_res is None:  # insertion
                resi = m_res.index
                resrange = self.residue_range(
                    f'{resi}:A', f'{resi}:A'
                )
                print(f'(automodel) Unfreezing {resi}A')
                mutations.append(resrange)

            elif t_res.name != m_res.name:
                resi = m_res.index
                resrange = self.residue_range(
                    f'{resi}:A', f'{resi}:A'
                )
                print(f'(automodel) Unfreezing {resi}A')
                mutations.append(resrange)

        if not mutations:
            # Dummy region of the ACE2 protein.
            # MODELLER needs something to optimize
            print('(automodel) unfreezing single residue')
            return selection(self.residue_range('580:A', '580:A'))

        return selection(mutations)